# 贡献指南

感谢你考虑为 PDBonnie 做出贡献！🎉

## 🐛 报告 Bug

提交 Issue 前请先：

1. 搜索 [已有 Issue](../../issues) 确认未被报告
2. 准备以下信息：
   - 操作系统及版本
   - Python 版本（如源码运行）
   - PDBonnie 版本（`python main.py --help` 查看或 `PDBonnie.exe` 文件版本）
   - 复现命令与完整输出
   - 预期行为与实际行为

## 💡 提交功能建议

请通过 Issue 描述：

- 该功能的使用场景
- 期望的 CLI 形式（如新增参数、命令）
- 是否愿意自行实现并提交 PR

## 🔧 提交 Pull Request

### 开发环境

```bash
git clone https://github.com/aria467/PDBonnie.git
cd PDBonnie
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install biopython click path requests
```

### 提交流程

1. Fork 本仓库并创建特性分支：`git checkout -b feature/your-feature`
2. 提交变更：`git commit -m "feat: add your feature"`
3. 推送到 Fork：`git push origin feature/your-feature`
4. 在 GitHub 上发起 Pull Request

### 提交信息规范

参考 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 仅文档变更
- `refactor:` 代码重构（非功能变更）
- `chore:` 构建流程、依赖更新等

### 代码风格

- 遵循 [PEP 8](https://peps.python.org/pep-0008/)
- 使用类型标注
- 公开函数添加 docstring

## 🧪 本地测试

```bash
# 基本功能
python main.py 3COM
python main.py 1BNA -f pdb

# 边缘情况
python main.py "!!!!"   # 应报错
python main.py "3com "  # 应自动 trim
```

## 📜 行为准则

请保持友善、专业的沟通环境。所有参与者均应遵守 [Contributor Covenant](https://www.contributor-covenant.org/zh-cn/version/2/1/code_of_conduct/)。