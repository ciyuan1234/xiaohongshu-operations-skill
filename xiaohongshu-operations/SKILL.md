---
name: xiaohongshu-operations
description: "Operate Xiaohongshu tech notes, visual cards and pacing."
version: 1.2.0
author: 秋安 (ciyuan1234), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [xiaohongshu, red, social-media, automation, creator, anti-ai, publishing, github-sync, wechat-sync]
    category: social-media
---

# Xiaohongshu Operations Skill

Operate Xiaohongshu (小红书) creator accounts for technology, developer, and productivity verticals. Enforces strict de-AI style rules, hybrid visual architecture (P1 high-CTR editorial poster + P2-Pn native proof), platform character limits, publishing pacing guardrails, dual-platform synchronization to WeChat Official Account ("小绿书" image-post), zero-drag monetization funnels, and automated GitHub open-source synchronization.

## When to Use

- Writing or reviewing Xiaohongshu notes in tech, programming, tools, or productivity domains.
- Auditing note drafts against platform limits (20-char title limit, 350-750 body characters).
- Running text linter checks (`scripts/lint.py`) to eliminate AI smells, corporate jargon, and banned marketing clichés.
- Checking publishing intervals and pacing gates (`scripts/guard.py`) to prevent spam penalties and account shadowbans.
- Preparing hybrid multi-slide carousels: P1 high-CTR Swiss editorial poster + P2-Pn real tool UI, GitHub repository, and project screenshots.
- Synchronizing notes directly to WeChat Official Account image-posts ("小绿书" `createType=8`) with character-safe adaptation.
- Designing zero-touch monetization loops (software licenses, curated digital checklists, verified partnerships).
- Synchronizing local skill updates to the open-source GitHub repository (`ciyuan1234/xiaohongshu-operations-skill`).

## Quick Reference

```bash
# Run local text linting against draft note
python3 scripts/lint.py drafts/note_example.md

# Inspect publish cadence and cooldown state
python3 scripts/guard.py check

# Record a published note to cadence guard
python3 scripts/guard.py record-note

# Synchronize a published note to WeChat Official Account draft box
python3 scripts/wechat_sync_publisher.py --note note_14

# Trigger immediate manual sync to GitHub
sync-skills
```

## Core Invariants & Rules

1. **Hybrid Visual Architecture (P1 Editorial Poster + P2-Pn Native Proof)**:
   - **P1 Cover (Feed CTR)**: Use high-CTR Swiss editorial typography posters. Clear pain points, bold headline typography, strict grid hierarchy, zero AI slop, and high contrast in mobile feeds.
   - **P2-Pn Inner Slides (Trust & Proof)**: Intersperse real macOS/Linux application UI, configuration presets, official product landing pages, and GitHub repository proof screenshots (Star counts, Release notes).
   - **Negative Rules**: Ban AI-generated illustrations (Midjourney/Flux) and tacky fake terminal mockups with synthetic traffic-light window frames. Combine high-impact typography covers with genuine technical proof.

2. **Platform Character Ceilings**:
   - **Xiaohongshu Title**: Strictly <= 20 characters (including punctuation). 21+ characters triggers platform rejection ("标题最多输入20字哦~").
   - **Xiaohongshu Body Length**: Maintain between 350 and 750 characters (platform floor 300, platform hard ceiling 1000). Evaluated after stripping tags and whitespace.

3. **WeChat Official Account Synchronization ("小绿书" / 贴图模式 `createType=8`)**:
   - **Title Byte Limit**: Strictly <= 20 half-width byte units (Chinese characters count as 2, ASCII as 1; maximum 10 Chinese characters). Exceeding this triggers platform modal error "标题长度不能超过20字".
   - **ProseMirror Selector Isolation**: The editor contains multiple ProseMirror instances. Target `.title-editor__input .ProseMirror` (or `window.__mpTitleEditor`) for the title, and `.share-text__input.js_pmEditorArea .ProseMirror` for the body. Targeting bare `.ProseMirror` dumps body text into the title.
   - **Cover Image Attachment**: Multi-step modal flow: Click `.js_imagedialog`, select item via `.image_dialog__checkbox`, click "下一步", then click "确认" before saving draft.
   - **Author & Hooks**: Author locked to "秋安kite", with organic first-person self-pickup lead hooks (【配置】、【远控】、【模型】、【压缩】、【截图】、【全套】).

4. **High-CTR Technical Topic Archetypes**:
   - Academic & thesis productivity: Zotero, Calibre, Obsidian, LaTeX workflows.
   - Developer offline Swiss-army knives: IT-Tools, DevToys, Lazygit, DBeaver (zero cloud privacy leak).
   - Modern terminal acceleration: Ghostty, Lazygit, Raycast, modern shell setups.
   - Extreme media & system optimization: HandBrake, LosslessCut, IINA, Stats, AppCleaner.

5. **Cadence & Anti-Ban Pacing Gate**:
   - Cold-Start (<8 posts): Strictly max 1 note/day, gap >= 20h, week <= 7 notes.
   - Growth (8+ approved posts, >700 views, >10% CTR): 2 notes/day, gap >= 6h (Morning 07:30–09:00, Evening 18:30–22:00).
   - High-Velocity: Up to 4 notes/day, gap >= 3h (08:45, 12:30, 18:15, 21:30).
   - Blackout Period: 00:00–07:00 CST (no posting).

6. **Zero-Touch Monetization**:
   - Curated lightweight digital assets ($9.9–$39 RMB) with automated delivery via self-pickup keywords in comments.
   - Software affiliate & license distribution (正版软件分销) organically referenced.
   - Strictly ban custom coding / freelance services (zero leverage).

7. **Automated GitHub Open-Source Synchronization**:
   - Local skill changes are symlinked directly to the Git repository.
   - The macOS LaunchAgent (`com.kite.skill-github-sync`) watches for modifications and runs tests before committing.

## Detailed References

- `references/visual_and_screenshot_sop.md`: Hybrid poster cover design, native screenshot sourcing, and cropping guidelines.
- `references/wechat_mp_sync.md`: WeChat Official Account image-post ("小绿书") automation, DOM selectors, and character limits.
- `references/algorithm_and_traffic.md`: Xiaohongshu explore feed CES ranking model and cohort testing.
- `references/de_ai_style_guide.md`: Complete de-AI writing guide, banned vocabulary, and sentence structures.
- `references/account_pacing_and_antiban.md`: Stage-based posting frequencies, cooldown triggers, and risk recovery.
- `references/high_ctr_topic_archetypes.md`: Proven high-bookmark content models in tech and productivity.
- `references/monetization_and_funnel.md`: Zero-drag commercialization and private-domain conversion loops.

## Step-by-Step Procedure

1. **Select Topic Archetype**:
   Pick a concrete friction point from `high_ctr_topic_archetypes.md` (e.g. video file size bloat, terminal shell navigation, paper citation sorting).

2. **Prepare Visual Carousel (Hybrid Model)**:
   - Generate P1 high-CTR Swiss editorial poster highlighting the core pain point and measurable payoff.
   - Capture clean, unadulterated screenshots of the real tool UI, configuration settings, and official GitHub repo.
   - Crop images to 3:4 ratio (1080x1440) using `scripts/crop_tool.py`.

3. **Draft Note Content**:
   - Write title adhering to `len(title) <= 20`.
   - Write body (350–750 characters) opening directly with real-world friction.
   - Conclude with an authentic self-pickup keyword prompt (e.g. 留【压缩】自取实操参数清单).

4. **Run Automated Linting & Cadence Check**:
   - Execute `python3 scripts/lint.py <draft_path>`.
   - Execute `python3 scripts/guard.py check`.

5. **Publish to Xiaohongshu**:
   - Submit through creator center via automated browser session.
   - Execute `python3 scripts/guard.py record-note`.

6. **Mirror to WeChat Official Account Draft Box**:
   - Execute `python3 scripts/wechat_sync_publisher.py --note <note_id>`.
   - Ensure title is truncated to <= 20 half-width characters.
   - Verify draft `appmsgid` is captured in history database.

## Pitfalls

- **Do not use raw UI screenshots alone as cover**: Feed CTR drops sharply without punchy headline typography; use a Swiss editorial poster as P1, then use raw UI screenshots as inner slides.
- **Do not target bare `.ProseMirror` in WeChat editor**: On `createType=8`, the first `.ProseMirror` is the title editor. Always target `.share-text__input.js_pmEditorArea .ProseMirror` for the body text to avoid dumping the article into the title.
- **Do not exceed 20 half-width characters in WeChat image-post titles**: Chinese characters count as 2; max 10 Chinese characters, otherwise platform blocks saving drafts.
- **Do not use salesy comment bait (\"评论区扣1领资料\")**: Triggers platform spam filtering; use neutral technical keywords like 【配置】、【压缩】、【远控】、【模型】.
- **Do not publish during midnight blackout (00:00–07:00 CST)**: Zero explore feed traffic, triggers automated nocturnal bot audits.
