# 小红书硬核技术博主全流程运营 Skill (Xiaohongshu Operations Skill)

[![Hermes Agent Skill](https://img.shields.io/badge/Hermes_Agent-Skill-blue.svg)](https://hermes-agent.nousresearch.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)
[![Tested with Unittest](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](xiaohongshu-operations/tests)

面向 **AI 编程、独立开发者、极客工具与学术生产力** 创作者的小红书（RED）全流程运营实战 Skill。

沉淀自真实运营测试与全自动流水线实践，旨在彻底解决技术博主在小红书上的四大核心痛点：
1. **被读者嘲讽「活人感满满」/ 被算法打标「AI 创作」**：缺乏真实细节、充斥营销大词与二元说教；
2. **图文排版被降权**：使用虚假仿 Finder/Terminal 营销卡片或 AI 概念图，导致完播率和点击率崩盘；
3. **触碰平台硬性红线**：标题超出 20 字被拒、正文字数不足 300 或超出 1000、频繁突发连发导致账号被风控限流；
4. **商业化陷入低杠杆陷阱**：在主页接私单做定制外包，被无休止改需求消耗殆尽。

---

## 🌟 核心能力架构

```
xiaohongshu-operations/
├── SKILL.md                          # Hermes Agent / Claude Code 技能标准规范
├── scripts/
│   ├── lint.py                       # 本地去 AI 感与平台合规自查门禁 (26 项硬禁 + 软警)
│   ├── guard.py                      # 账号生命周期发布节律守卫 (冷启动/成长期/高频期防封)
│   └── crop_tool.py                  # macOS/Linux 3:4 原生画幅截图无损裁剪工具
├── references/
│   ├── algorithm_and_traffic.md       # CES 评分模型、流量池层级与冷启动生死 2 小时
│   ├── de_ai_style_guide.md           # 去 AI 感文风实战：句式禁令、微观摩擦与同侪视角
│   ├── visual_and_screenshot_sop.md   # 真机原生截图标准：严禁合成卡片与 AI 图
│   ├── account_pacing_and_antiban.md  # 每日/周上限、黑时段与异常 48h 风险冷却机制
│   ├── high_ctr_topic_archetypes.md   # 三大高留藏选题模型 (学术双链/离线瑞士军刀/现代终端)
│   └── monetization_and_funnel.md     # 零交付变现闭环：正版分销、数字资产与主页暗号
└── templates/
    ├── note_technical_tool.md         # 开发者离线工具实测笔记模版
    ├── note_academic_productivity.md  # 学术双链与文献管理笔记模版
    └── note_terminal_workflow.md      # 现代终端与提效工作流笔记模版
```

---

## 🚀 核心铁律与实战机制

### 1. 严格「去 AI 感」与同侪视角 (Zero AI Slop)
- **封杀合成宣传卡片**：严禁使用 AI 绘图或带有 macOS 交通灯红黄绿圆点的假窗口模板（读者一眼判定为营销号）。只采用真机原生截图（`screencapture -x`）、官方 GitHub 仓库页面或真实报错日志。
- **开门见山，微观摩擦切入**：严禁宏大叙事（「5款AI神器大盘点」），直接从真实工位摩擦切入（如「天天用 Claude Code，顺手查磁盘发现偷吃了 3.2GB 缓存」）。
- **绝对禁词库**：硬禁「不是A而是B」、「深层来看」、「赋能/底层逻辑/闭环」、「颠覆性/封神/亲测有效」等 26 种 AI/营销套话。

### 2. 平台字符物理红线
- **标题硬限**：严格校验 `len(title) <= 20` 字（包含标点符号）。超过 20 字小红书前端直接弹出「标题最多输入20字哦~」阻断发布。
- **正文字数区间**：严格控制在 **350 - 750 字** 之间（平台底线 300 字，硬上限 1000 字）。

### 3. 发布节律与风控守卫 (Cadence Guard)
根据账号生命周期动态调度，内置夜间黑时段与安全冷却：
- **冷启动期 (<8篇)**：每日严格限 1 篇，发布间隔 ≥ 20 小时，每周 ≤ 7 篇；
- **成长期 (正常状态)**：每日 2 篇（早通勤 07:30–09:00 + 晚黄金档 18:30–22:00），发布间隔 ≥ 6 小时；
- **夜间黑时段**：00:00 - 07:00 (CST) 强制禁发，防夜间异常扫描与无效曝光。

### 4. 零交付变现闭环 (Zero-Drag Monetization)
- **坚决封杀外包写代码**：定制开发需求蔓延严重、零杠杆且易引发违规。
- **自动化数字履约**：
  1. 正版软件授权分销（数码荔枝等，佣金 15%-35%）；
  2. 极客自用配置清单与避坑手册（¥9.9 - ¥39.9 薯店/面包多自动发卡）；
  3. 千粉官方蒲公英商业合作；
  4. 主页自然留白引流至同名深度技术生态。

---

## 🛠️ 快速上手与 CLI 工具使用

### 一键安装到 Hermes Agent / Claude Code
```bash
git clone https://github.com/ciyuan1234/xiaohongshu-operations-skill.git
cd xiaohongshu-operations-skill

# 安装到本地 Hermes Agent 技能目录 (~/.hermes/skills/social-media/)
./install.sh
```

Windows PowerShell 用户：
```powershell
.\install.ps1
```

### 1. 运行本地草稿合规自查 (`lint.py`)
在发布前执行本地自动化审核，拦截超长标题、字数违规与 AI 腔调：
```bash
python3 xiaohongshu-operations/scripts/lint.py xiaohongshu-operations/templates/note_technical_tool.md
```
输出示例：
```
============================================================
 Xiaohongshu Note Linter Report
============================================================
[*] 标题长度: 20 字 (上限 20 字) -> 「Mac离线接口调试，换到Bruno清静了」
[*] 正文字数: 421 字 (推荐 350-750 字)
[*] Emoji 统计: 共 0 个 / 0 种
[*] 具体数值/版本/时间证据: 3 处
[*] 话题标签: 4 个

Result: LINT PASSED
```

### 2. 检查发布节奏与防封状态 (`guard.py`)
```bash
# 检查当前是否允许发布
python3 xiaohongshu-operations/scripts/guard.py check

# 记录一次发布行为
python3 xiaohongshu-operations/scripts/guard.py record-note

# 切换为成长期模式
python3 xiaohongshu-operations/scripts/guard.py set-mode growth

# 若遭遇审核异常，开启 48 小时安全冷却
python3 xiaohongshu-operations/scripts/guard.py set-cooldown 48
```

### 3. 原生截图一键裁剪至 3:4 画幅 (`crop_tool.py`)
```bash
# 自动居中裁切并缩放到标准 1080x1440
python3 xiaohongshu-operations/scripts/crop_tool.py --input raw_terminal.png --output cover.png
```

---

## 🧪 单元测试

本项目提供完备的单元测试，覆盖所有禁词、字数越界检测与发布节律状态：
```bash
python3 -m unittest discover -s xiaohongshu-operations/tests -p "test_*.py"
```

---

## 📄 开源许可证

本项目基于 [MIT License](LICENSE) 开源。欢迎 Star、Fork 与提 PR 共同完善极客创作者生态！
