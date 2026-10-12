---
name: xiaohongshu-operations
description: "Operate Xiaohongshu tech notes, visual cards and pacing."
version: 1.0.0
author: 秋安 (ciyuan1234), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [xiaohongshu, red, social-media, automation, creator, anti-ai, publishing]
    category: social-media
---

# Xiaohongshu Operations Skill

Operate Xiaohongshu (小红书) creator accounts for technology, developer, and productivity verticals. Enforces strict de-AI style rules, native screen capture standards, platform character limits, publishing pacing guardrails, and zero-drag monetization funnels.

## When to Use

- Writing or reviewing Xiaohongshu notes in tech, programming, tools, or productivity domains.
- Auditing note drafts against platform limits (20-char title limit, 350-750 body characters).
- Running text linter checks (`scripts/lint.py`) to eliminate AI smells, corporate jargon, and banned marketing clichés.
- Checking publishing intervals and pacing gates (`scripts/guard.py`) to prevent spam penalties and account shadowbans.
- Preparing unadulterated 3:4 ratio real UI screenshots instead of synthetic HTML mockup cards.
- Designing zero-touch monetization loops (software licenses, curated digital checklists, verified partnerships).
- Don't use for: generic marketing ad spam, automated comment begging ("扣1领资料"), or low-leverage freelance coding outsourcing.

## Prerequisites

- Python 3.9+ (Python 3.10+ recommended) for running local linting and guard verification scripts.
- Image processing utility: `sips` (macOS native) or `Pillow` / `ImageMagick` for cropping captures to 3:4 aspect ratio (1080x1440).
- Platform account: Xiaohongshu creator account (`creator.xiaohongshu.com`).

## Quick Reference

```bash
# Run local text linting against draft note
python3 scripts/lint.py drafts/note_example.md

# Inspect publish cadence and cooldown state
python3 scripts/guard.py check

# Record a published note to cadence guard
python3 scripts/guard.py record-note

# Crop image to standard 3:4 ratio (1080x1440)
python3 scripts/crop_tool.py --input screenshot.png --output cover.png
```

## Core Invariants & Rules

1. **Zero AI-Slop & Authentic Peer Voice**:
   - Strictly ban synthetic HTML/CSS mockup cards (Finder/Terminal templates with traffic-light dots) and AI-generated illustrations. Readers immediately recognize them as automated content farms.
   - Only use pristine native desktop screen crops (`screencapture -x`), official GitHub repository headers, or official tool landing pages.
   - Speak as an authentic junior developer / independent builder sharing genuine friction, configuration nuances, and surprises.
   - Ban didactic lectures ("你应该", "作为一个程序员", "深度剖析"), binary rhetorical contrasts ("不是A而是B"), and marketing buzzwords ("底层逻辑", "颠覆", "降维打击").

2. **Platform Character Ceilings**:
   - **Title**: Strictly <= 20 characters (including punctuation). Any title with 21+ characters triggers platform rejection ("标题最多输入20字哦~").
   - **Body Length**: Maintain between 350 and 750 characters (platform floor 300, platform hard ceiling 1000). Evaluated after stripping tags and whitespace.

3. **High-CTR Technical Topic Archetypes**:
   - Academic & thesis productivity: Zotero, Calibre, Obsidian, LaTeX workflows.
   - Developer offline Swiss-army knives: IT-Tools, DevToys, Lazygit, DBeaver (zero cloud privacy leak).
   - Modern terminal acceleration: Ghostty, Lazygit, Raycast, modern shell setups.

4. **Cadence & Anti-Ban Pacing Gate**:
   - Cold-Start (<8 posts): Strictly max 1 note/day, gap >= 20h, week <= 7 notes.
   - Growth (8+ approved posts, >700 views, >10% CTR): 2 notes/day, gap >= 6h (Morning 07:30–09:00, Evening 18:30–22:00).
   - High-Velocity: Up to 4 notes/day, gap >= 3h (08:45, 12:30, 18:15, 21:30).
   - Blackout Period: 00:00–07:00 CST (no posting).

5. **Zero-Touch Monetization**:
   - Software affiliate & license distribution (正版软件分销/数码荔枝) organically referenced in profile or comments.
   - Curated lightweight digital assets ($9.9–$39 RMB) with automated delivery.
   - Strictly ban custom coding / freelance services (endless scope creep, zero leverage).

## Detailed References

- `references/algorithm_and_traffic.md`: Xiaohongshu explore feed CES ranking model and cohort testing.
- `references/de_ai_style_guide.md`: Complete de-AI writing guide, banned vocabulary, and sentence structures.
- `references/visual_and_screenshot_sop.md`: Screenshot sourcing, native cropping, and visual proof guidelines.
- `references/account_pacing_and_antiban.md`: Stage-based posting frequencies, cooldown triggers, and risk recovery.
- `references/high_ctr_topic_archetypes.md`: Proven high-bookmark content models in tech and productivity.
- `references/monetization_and_funnel.md`: Zero-drag commercialization and private-domain conversion loops.

## Step-by-Step Procedure

1. **Select Topic Archetype**:
   Pick a concrete friction point from `high_ctr_topic_archetypes.md` (e.g. disk cache explosion from AI CLIs, offline JSON formatters, paper citation sorting).

2. **Prepare Visual Proof (Cover & Carousel)**:
   - Run the tool locally or open the official GitHub repository.
   - Capture clean, unadulterated screenshots using native tools.
   - Crop to 3:4 ratio (1080x1440) using `scripts/crop_tool.py`.
   - Never add decorative borders, banners, badge tags, or slide numbers (`1/4`).

3. **Draft Note Content**:
   - Write title adhering to `len(title) <= 20`.
   - Write body (350–750 characters) opening directly with real-world friction.
   - Include concrete commands (`brew install ...`), exact configuration paths, or measurable observations.
   - Conclude with an open-ended peer-to-peer sharing prompt.

4. **Run Automated Linting**:
   - Execute `python3 scripts/lint.py <draft_path>`.
   - Fix any `FAIL` errors (title > 20, body < 300, hard banned words).
   - Review `WARN` notices (emoji density, excessive list items, missing specific figures).

5. **Check Cadence Guard**:
   - Execute `python3 scripts/guard.py check`.
   - If `allowed: false`, respect `wait_seconds` and defer publishing.

6. **Publish & Record**:
   - Submit through creator center or automated browser session.
   - Execute `python3 scripts/guard.py record-note` to log the publish timestamp.

## Pitfalls

- **Do not wrap screenshots in synthetic HTML templates**: Readers immediately spot synthetic card wrappers (e.g. fake macOS window frames) and downvote as marketing spam.
- **Do not use salesy comment bait ("评论区扣1领资料")**: Triggers platform spam filtering and reduces organic recommendation weights.
- **Do not hardcode absolute paths**: Always use repo-relative paths for assets and scripts.
- **Do not publish during midnight blackout (00:00–07:00 CST)**: Zero explore feed traffic, triggers automated nocturnal bot audits.

## Verification

- Linter passes clean: `python3 scripts/lint.py <draft>` exits with code 0.
- Pacing gate confirms: `python3 scripts/guard.py check` returns `"allowed": true`.
- Output image is valid 3:4 ratio (1080x1440 or 1200x1600).
- Title character count <= 20 characters verified.
