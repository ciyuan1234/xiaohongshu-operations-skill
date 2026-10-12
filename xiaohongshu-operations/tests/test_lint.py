#!/usr/bin/env python3
"""Unit tests for Xiaohongshu linter."""

import unittest
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from lint import check_text


class TestXiaohongshuLinter(unittest.TestCase):
    def test_clean_good_note_passes(self):
        good_text = """标题: 终端换到Ghostty，字体渲染很舒服

天天在终端里跑自动化脚本和编译，旧终端开多了风扇容易狂转，特别是在大缓冲区滚屏时有明显的掉帧感。

最近把主力终端切到了Ghostty 1.0，直接用原生Metal GPU硬件加速。实测日常编译滚动几千行日志，帧率稳稳跑在120fps，CPU占用率从之前的18%降到了3%左右。

自用觉得比较顺手的几个点：
1. 原生跨平台与平滑渲染：SF Mono字体在Retina屏上的显示质感非常扎实，连字符支持得很自然。
2. 零外部依赖：单二进制文件直接运行，不需要装一堆重型框架或 Electron 运行时。
3. 搭配Lazygit操作Git分支，键盘快捷键响应延迟实测在4ms以内，盲按提交很顺畅。

完整的无冗余config配置只有30行，大家日常Mac上写代码最常用的终端是哪款？

#程序员日常 #开发者工具 #Mac实用软件
"""
        res = check_text(good_text)
        self.assertTrue(res["passed"], f"Expected pass but got fails: {res['fails']}")

    def test_title_too_long_fails(self):
        text_long_title = """标题: 这个标题故意写得超级长远远超过了二十个字的平台最高硬性上限规定啊

正文内容测试字数足够的一段话。这里写一些日常实测的内容，字数要超过三百字以满足平台的字数底线要求。
最近把主力终端切到了Ghostty 1.0，直接用原生Metal GPU加速。实测日常编译滚动几千行日志，帧率稳稳跑在120fps，CPU占用率从之前的18%降到了3%左右。
原生跨平台与平滑渲染，字体在Retina屏上的显示质感非常扎实。零外部依赖，单二进制文件直接运行，不需要装一堆重型框架。
搭配Lazygit操作Git分支，键盘快捷键响应延迟实测在4ms以内，盲按提交很顺畅。
大家日常写代码最常用的终端是哪款？
"""
        res = check_text(text_long_title)
        self.assertFalse(res["passed"])
        self.assertTrue(any("标题超长" in f for f in res["fails"]))

    def test_hard_banned_phrases_fail(self):
        text_with_bans = """标题: 测试违禁词拦截逻辑

这不是一款普通的工具，而是颠覆性的神器！点赞收藏不迷路，加我微信领资料。
正文内容测试字数足够的一段话。这里写一些日常实测的内容，字数要超过三百字以满足平台的字数底线要求。
最近把主力终端切到了Ghostty 1.0，直接用原生Metal GPU加速。实测日常编译滚动几千行日志，帧率稳稳跑在120fps，CPU占用率从之前的18%降到了3%左右。
原生跨平台与平滑渲染，字体在Retina屏上的显示质感非常扎实。零外部依赖，单二进制文件直接运行，不需要装一堆重型框架。
大家日常写代码最常用的终端是哪款？
"""
        res = check_text(text_with_bans)
        self.assertFalse(res["passed"])
        fail_reasons = " ".join(res["fails"])
        self.assertIn("不是A而是B", fail_reasons)
        self.assertIn("站外引流", fail_reasons)

    def test_too_short_body_fails(self):
        text_too_short = """标题: 短标题测试

字数太少了，只有这一句话。
"""
        res = check_text(text_too_short)
        self.assertFalse(res["passed"])
        self.assertTrue(any("字数过少" in f for f in res["fails"]))


if __name__ == "__main__":
    unittest.main()
