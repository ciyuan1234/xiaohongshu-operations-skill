# Xiaohongshu Operations Skill for AI & Tech Builders

[![Hermes Agent Skill](https://img.shields.io/badge/Hermes_Agent-Skill-blue.svg)](https://hermes-agent.nousresearch.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)
[![Tested with Unittest](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](xiaohongshu-operations/tests)

A battle-tested creator operations Skill designed for **AI developers, independent builders, terminal geeks, and academic productivity creators** publishing on Xiaohongshu (RED).

Distilled from real-world operations and autonomous agent pipelines, this Skill solves four critical pain points faced by technical creators:
1. **Readers mocking content as AI-generated ("活人感满满") or algorithms tagging posts as AI slop**: Lack of messy real-world friction, didactic tone, and corporate marketing jargon;
2. **Algorithmic suppression from synthetic visuals**: Synthetic HTML/Finder card wrappers with traffic-light dots or AI illustrations resulting in collapsed click-through and completion rates;
3. **Triggering hard platform boundaries**: Titles exceeding the 20-character ceiling, body text under 300 or over 1000 characters, and rapid burst-posting triggering spam shadowbans;
4. **Falling into low-leverage monetization traps**: Taking on custom freelance coding contracts with endless scope creep and zero leverage.

---

## 🌟 Core Architecture

```
xiaohongshu-operations/
├── SKILL.md                          # Hermes Agent / Claude Code skill specification
├── scripts/
│   ├── lint.py                       # Automated de-AI linter & compliance gate (26 hard bans + soft rules)
│   ├── guard.py                      # Lifecycle cadence & anti-ban guard (cold-start/growth/pacing)
│   └── crop_tool.py                  # macOS/Linux native 3:4 aspect ratio lossless cropper
├── references/
│   ├── algorithm_and_traffic.md       # CES scoring model, tier migration & the crucial 2h cold-start window
│   ├── de_ai_style_guide.md           # De-AI writing guide: sentence patterns, micro-scenes & peer voice
│   ├── visual_and_screenshot_sop.md   # Pristine screen captures: ban synthetic cards & AI art
│   ├── account_pacing_and_antiban.md  # Daily/weekly limits, blackout hours & 48h risk cooldown
│   ├── high_ctr_topic_archetypes.md   # 3 high-bookmark topic models (academic/offline Swiss-army/terminals)
│   └── monetization_and_funnel.md     # Zero-drag monetization: software affiliates & curated digital assets
└── templates/
    ├── note_technical_tool.md         # Developer offline utility note template
    ├── note_academic_productivity.md  # Academic literature bi-directional linking template
    └── note_terminal_workflow.md      # Modern shell & GPU-accelerated terminal template
```

---

## 🚀 Key Rules & Invariants

### 1. Zero AI Slop & Authentic Peer Voice
- **Ban Decorative Card Wrappers**: Never wrap screenshots in synthetic HTML/CSS templates or fake macOS window frames. Use uncut native OS screen captures (`screencapture -x`), official GitHub headers, or raw terminal buffers.
- **Micro-Scenes over Macro-Listicles**: Never post generic listicles ("5 Best AI Tools"). Focus on a single workplace friction point (e.g. "Running Claude Code and Codex daily, checked Mac disk storage and found 3.2GB cached").
- **Strict Banned Vocabulary**: Enforce hard bans on 26 cliché patterns ("不是A而是B", "深层来看", "赋能/底层逻辑/闭环", "颠覆/封神/亲测有效").

### 2. Platform Character Limits
- **Title Ceiling**: Strictly `len(title) <= 20` characters (including punctuation). Titles with 21+ characters are blocked with platform toasts.
- **Body Character Range**: Maintain strictly between **350 and 750 characters** (platform floor 300, platform hard ceiling 1000).

### 3. Pacing & Anti-Ban Guard (`guard.py`)
- **Cold-Start Phase (<8 posts)**: Max 1 note/day, gap >= 20h, week <= 7 notes;
- **Growth Phase**: 2 notes/day (Morning 07:30–09:00 + Evening 18:30–22:00), gap >= 6h;
- **Midnight Blackout**: 00:00–07:00 CST strictly blocked to avoid abnormal bot audits.

### 4. Zero-Drag Monetization Loop
- **Ban Freelance Coding**: Custom coding is zero-leverage, has endless scope creep, and risks platform violations.
- **Automated Digital Assets**: Curated tool checklists, software license affiliate links, and automated fulfillment.

---

## 🛠️ Quick Start

### One-Click Installation
```bash
git clone https://github.com/ciyuan1234/xiaohongshu-operations-skill.git
cd xiaohongshu-operations-skill

# Install into Hermes Agent skills directory (~/.hermes/skills/social-media/)
./install.sh
```

Windows PowerShell:
```powershell
.\install.ps1
```

### 1. Run Automated Linter
```bash
python3 xiaohongshu-operations/scripts/lint.py xiaohongshu-operations/templates/note_technical_tool.md
```

### 2. Check Cadence Guard
```bash
python3 xiaohongshu-operations/scripts/guard.py check
python3 xiaohongshu-operations/scripts/guard.py record-note
python3 xiaohongshu-operations/scripts/guard.py set-mode growth
```

### 3. Crop Native Screenshots to 3:4 (1080x1440)
```bash
python3 xiaohongshu-operations/scripts/crop_tool.py --input raw_terminal.png --output cover.png
```

---

## 🧪 Unit Testing

Run the full test suite verifying lint rules and cadence logic:
```bash
python3 -m unittest discover -s xiaohongshu-operations/tests -p "test_*.py"
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
