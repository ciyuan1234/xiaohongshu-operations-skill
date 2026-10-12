#!/usr/bin/env python3
"""Xiaohongshu note text linter.

Enforces de-AI writing standards, title character ceiling (<=20),
body character range (300-1000), paragraph pacing, and banned phrases.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Any

# Hard ban rules: triggers instant failure
HARD_BANS = [
    (r"不是[^。\n]{0,20}，?\s*而是", "§2 不是A而是B（经典二元说教句式）"),
    (r"并非[^。\n]{0,20}，?\s*而是", "§2 并非A而是B（经典二元说教句式）"),
    (r"与其说[^。\n]{0,25}，?\s*不如说", "§2 与其说不如说（机械对比）"),
    (r"综上所述|总而言之|总的来说", "§2 总结套话（公文体/AI腔）"),
    (r"值得注意的是|众所周知|不难发现|不可否认", "§2 空转过渡套话"),
    (r"让我们拭目以待|让我们一起|一起来看看", "§2 舞台营销腔"),
    (r"这背后反映的是|深层来看|追根究底|究其本质", "§2 强行升华与抽象拔高"),
    (r"作为一名|从业\s*\d+\s*年来", "§2 借身份压人说教"),
    (r"在[^。\n]{0,15}的今天|随着[^。\n]{0,15}的发展", "§2 宏大叙事开头套话"),
    (r"你怎么看|你怎么评价|欢迎在?评论区|对此[，,]?\s*你", "§2 反问求互动（营销痕迹）"),
    (r"点赞收藏|关注我|求三连|不迷路|一键三连", "§2 强行索求互动（触发限流）"),
    (r"赋能|抓手|闭环|底层逻辑|颗粒度|心智[模型]?|降维打击|碾压|吊打|封神", "§2 互联网黑话与夸大词"),
    (r"颠覆性|革命性|里程碑意义|未来可期|前景广阔|潜力巨大", "§2 夸大其词公关腔"),
    (r"深入探讨|深度剖析|全面解读|全方位把握", "§2 空洞公文词汇"),
    (r"至关重要|举足轻重|不可或缺", "§2 溢美辞藻"),
    (r"实际上，?首先|首先[，,].{0,30}其次[，,].{0,30}最后[，,]", "§2 机械三段式结构"),
    (r"(?m)^#{1,6}\s", "§1C Markdown标题行（小红书App渲染为乱码或井号）"),
    (r"(?m)^\|.*\|", "§1C Markdown表格（小红书移动端排版碎裂）"),
    (r"震惊|99% 的人|99%的人|最后一天|速看|不转不是", "§1C 低质标题党/平台违禁词"),
    (r"https?://|www\.\S+\.\S+|二维码|加我微信|私我|私信领", "§1C 站外引流违规词（重度限流）"),
    (r"🚀|💡|✅|❌|→|⬇️|🔥|📈", "§4 营销符号/箭头清单墙装饰"),
    (r"(?m)^- \*\*[^*\n]{1,20}[:：]", "§2 加粗标签清单排比体"),
    (r"希望这篇(内容)?(能|对)?(帮|有用)|欢迎指正|欢迎交流", "§2 谄媚客套套话"),
    (r"如果觉得有用|点个赞|求赞", "§2 乞赞套话"),
    (r"差点被惊呆|吓尿了|大起底|避坑警告|亲测有效", "§2 夸张营销震颤词"),
    (r"评论区扣|留【自用】|留【装机】|留【配置】|带你快速变现", "§2 诱导互动与黑产引流模版"),
]

# Soft warning rules: warning thresholds
SOFT_WARNS = [
    (r"——", "§2 破折号过多", 2),
    (r"！{2,}|!{2,}", "§2 连续感叹号", 0),
    (r"首先[，,]|其次[，,]", "§2 首先其次过度使用", 1),
    (r"不仅[^。\n]{0,25}，?\s*(而且|更|也)", "§2 不仅而且递进排比", 1),
    (r"其实[^。\n]{0,10}不是[^。\n]{0,15}，(而)?是", "§1 变体不是而是句式", 0),
]

SPECIFIC_FIGURES = re.compile(
    r"\d+(?:\.\d+)?%|\$\d+|\d+[KkMm]?\s*(?:token|美元|美金|次|万|K|MB|GB|TB|ms|s)|v?\d+\.\d+(?:\.\d+)?|\d{4}\s*年"
)

EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⬀-⯿]"
)

TITLE_RE = re.compile(r"^\s*(?:title|标题)\s*[:：]\s*(.+)$", re.M | re.I)


def count_sentences(paragraph: str) -> int:
    parts = [p for p in re.split(r"[。！？!?；;]", paragraph) if p.strip()]
    return len(parts) if parts else (1 if paragraph.strip() else 0)


def check_text(text: str) -> dict[str, Any]:
    fails: list[str] = []
    warns: list[str] = []
    notes: list[str] = []

    # Clean image comments: <!--img:...-->
    clean_text = re.sub(r"<!--img:[^>]*-->\n?", "", text)

    # Title extraction and verification
    m = TITLE_RE.search(clean_text)
    if m:
        title = m.group(1).strip().strip("\"'“”")
        tlen = len(re.sub(r"\s", "", title))
        notes.append(f"标题长度: {tlen} 字 (上限 20 字) -> 「{title}」")
        if tlen > 20:
            fails.append(f"§3 标题超长: {tlen} 字 > 平台硬限 20 字 (「{title}」)")
        body = clean_text[: m.start()] + clean_text[m.end():]
    else:
        # Check first line as potential title if not explicitly labeled
        lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
        if lines:
            first = lines[0]
            if len(first) <= 30 and not first.startswith(("#", "-", "*", ">")):
                tlen = len(re.sub(r"\s", "", first))
                notes.append(f"检测首行为标题: {tlen} 字 -> 「{first}」")
                if tlen > 20:
                    fails.append(f"§3 标题超长: 首行推断标题 {tlen} 字 > 20 字")
                body = "\n".join(lines[1:])
            else:
                warns.append("§3 未找到显式「标题:」标头")
                body = clean_text
        else:
            warns.append("§3 内容为空")
            body = clean_text

    # Hard ban checks
    for pat, label in HARD_BANS:
        for mm in re.finditer(pat, body, re.M):
            ctx = body[max(0, mm.start() - 12): mm.end() + 12].replace("\n", " ")
            fails.append(f"{label} -> 「…{ctx}…」")

    # Soft warning checks
    for pat, label, limit in SOFT_WARNS:
        matches = len(re.findall(pat, body))
        if matches > limit:
            warns.append(f"{label}: 出现 {matches} 次 (警戒阈值 {limit})")

    # Character count checks (body only, no spaces)
    chars = len(re.sub(r"\s", "", body))
    notes.append(f"正文字数: {chars} 字 (推荐 350-750 字)")
    if chars < 300:
        fails.append(f"§4 字数过少: 正文纯字数 {chars} < 300（平台图文评级底线）")
    if chars > 1000:
        fails.append(f"§4 字数超出: 正文纯字数 {chars} > 1000（平台硬性截断上限）")

    # Paragraph structure check
    paragraphs = [p.strip() for p in body.split("\n") if p.strip() and not p.strip().startswith("#")]
    longest, longest_sample = 0, ""
    for p in paragraphs:
        if re.match(r"^[-*]\s|^\d+[.、]\s", p):
            continue
        n = count_sentences(p)
        if n > longest:
            longest, longest_sample = n, p[:40]
    if longest > 3:
        warns.append(f"§4 单段过长: 最长段落含 {longest} 句 (建议 <=3 句保持呼吸感) -> 「{longest_sample}…」")

    # Emoji density checks
    emojis = EMOJI_PATTERN.findall(body)
    kinds = set(emojis)
    notes.append(f"Emoji 统计: 共 {len(emojis)} 个 / {len(kinds)} 种")
    if len(kinds) > 6:
        warns.append(f"§3 Emoji 种类过多: {len(kinds)} > 6 (花哨容易产生模板号观感)")

    wall_run, max_wall = 0, 0
    for p in body.split("\n"):
        if p.strip() and EMOJI_PATTERN.match(p.strip()):
            wall_run += 1
            max_wall = max(max_wall, wall_run)
        else:
            wall_run = 0
    if max_wall >= 3:
        warns.append(f"§1C 行首 Emoji 连续 {max_wall} 行构成符号墙")

    # Specific figures check
    spec_matches = len(SPECIFIC_FIGURES.findall(body))
    notes.append(f"具体数值/版本/时间证据: {spec_matches} 处")
    if spec_matches < 3:
        warns.append(f"§3 缺乏具象参数证据: 仅发现 {spec_matches} 处版本/体积/耗时等实测参数 (建议 >=3 处)")

    # Stance and opinion words
    stance_matches = len(
        re.findall(
            r"是倒退|不推荐|慎用|别用|没必要|不划算|最贵|坑|跑偏|不够|实测|崩溃|翻车|踩坑|更舒服|省事",
            body,
        )
    )
    if stance_matches == 0:
        warns.append("§3 未检测到鲜明态度词汇 (避免中庸平淡的「各有千秋」)")

    # Tags check
    tags = re.findall(r"#([^\s#]{1,20})", body)
    notes.append(f"话题标签: {len(tags)} 个")
    if len(tags) > 5:
        warns.append(f"§4 话题标签过多: {len(tags)} 个 > 建议上限 5 个")

    return {
        "passed": len(fails) == 0,
        "fails": fails,
        "warns": warns,
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Xiaohongshu note text linter")
    parser.add_argument("path", nargs="?", help="Markdown or text draft file path")
    parser.add_argument("--text", help="Raw draft text to inspect directly")
    args = parser.parse_args()

    if args.text:
        content = args.text
    elif args.path:
        if not os.path.exists(args.path):
            print(f"Error: file not found at '{args.path}'", file=sys.stderr)
            return 2
        with open(args.path, encoding="utf-8") as f:
            content = f.read()
    else:
        parser.print_help()
        return 2

    res = check_text(content)

    print("=" * 60)
    print(" Xiaohongshu Note Linter Report")
    print("=" * 60)
    for note in res["notes"]:
        print(f"[*] {note}")

    if res["warns"]:
        print("\n[!] WARNINGS (软警告建议改进):")
        for w in res["warns"]:
            print(f"  - {w}")

    if res["fails"]:
        print("\n[x] FAILURES (硬性阻断必须修正):")
        for f in res["fails"]:
            print(f"  - {f}")
        print("\nResult: LINT FAILED")
        return 1
    else:
        print("\nResult: LINT PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
