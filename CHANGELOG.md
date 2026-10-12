# Changelog

All notable changes to the `xiaohongshu-operations-skill` project will be documented in this file.

## [1.0.0] - 2026-10-12

### Initial Open-Source Release
- **Core Skill Spec**: Release `xiaohongshu-operations/SKILL.md` compliant with Hermes Agent, Claude Code, and OpenCode workflows.
- **De-AI Linter**: Standalone `lint.py` enforcing title 20-char limit, 350-750 body characters, emoji density control, and hard/soft bans.
- **Cadence Guard**: Stateful `guard.py` implementing stage-based rate limits (cold start, growth, high-velocity), midnight blackout, and 48h risk cooldown.
- **Visual Standards**: Native OS screenshot and 3:4 ratio cropping tool (`crop_tool.py`), banning synthetic HTML/Finder mockups.
- **Reference Playbooks**:
  - `algorithm_and_traffic.md`: CES scoring model and cohort testing.
  - `de_ai_style_guide.md`: Strict de-AI writing guide and banned vocabulary.
  - `visual_and_screenshot_sop.md`: Screenshot sourcing and pixel-perfect cropping.
  - `account_pacing_and_antiban.md`: Stage-based publishing intervals and risk management.
  - `high_ctr_topic_archetypes.md`: Proven high-bookmark topic models in tech/productivity.
  - `monetization_and_funnel.md`: Zero-drag commercialization and zero custom coding rule.
- **Templates**: Production-grade note templates for developer tools, academic literature workflows, and terminal configurations.
- **Automated Tests**: 100% passing unit tests under Python `unittest`.
