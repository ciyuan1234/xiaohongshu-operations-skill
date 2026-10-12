# Contributing to Xiaohongshu Operations Skill

欢迎对本项目做出贡献！为了保持高质、真实与平台安全，请遵守以下规范：

## 提交准则 (Contribution Standards)

1. **真实性第一**：所有规范必须基于真实的实机测试、真实平台规则变化或官方政策，严禁凭空臆造或合成虚假数据。
2. **零 AI 腔调**：禁止引入任何公文体套话、空洞黑话（如「赋能/底层逻辑」）或教条主义建议。
3. **代码与测试完备**：修改 `scripts/` 下的脚本（`lint.py`、`guard.py` 等）必须同步更新 `tests/` 中的单元测试，且保证 `python3 -m unittest` 全部通过。
4. **路径中立性**：严禁在代码与文档中硬编码个人本地绝对路径（如 `/Users/...` 或 `/home/...`），统一使用相对路径或环境变量。

## 提交流程 (Pull Request Workflow)

1. Fork 本仓库并新建分支：`git checkout -b feature/your-feature-name`
2. 运行自动化检查与单元测试：
   ```bash
   python3 -m unittest discover -s xiaohongshu-operations/tests -p "test_*.py"
   ```
3. 提交变更并推送：`git commit -m "feat: add ..."`
4. 发起 Pull Request，详细描述修改动机与实测验证结果。
