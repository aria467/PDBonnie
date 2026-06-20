# PDBonnie

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Release](https://img.shields.io/github/v/release/aria467/PDBonnie)](../../releases)


一个简单、快速的命令行工具，用于从 [RCSB PDB](https://www.rcsb.org/) 数据库下载蛋白质三维结构文件。基于 [Biopython](https://biopython.org/) 和 [Click](https://click.palletsprojects.com/) 构建。


## 📋 支持的格式

| 格式 | 文件扩展名 | 说明 |
|------|-----------|------|
| `mmcif` (默认) | `.cif` | mmCIF 格式，PDB 现行标准 |
| `pdb` | `.ent` | 传统 PDB 格式 |
| `xml` | `.xml` | PDBML/XML 格式 |
| `mmtf` | `.mmtf` | 压缩的二进制格式 |
| `bundle` | `.tar.gz` | PDBx/mmCIF 打包文件 |


## ⚡ 快速开始

### 方式一：使用预编译二进制文件（推荐）

从 [Releases](../../releases) 页面下载对应平台的 `PDBonnie` 可执行文件，即可直接运行：

```bash
# Windows
.\PDBonnie.exe 3COM
```

```bash
# macOS / Linux
./PDBonnie 3COM
```

### 方式二：从源码运行

**环境要求**：Python 3.12+

```bash
# 1. 克隆仓库
git clone https://github.com/aria467/PDBonnie.git
cd PDBonnie

# 2. 创建虚拟环境（推荐）
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. 安装依赖
pip install biopython click path requests

# 4. 运行
python main.py 3COM
```


## 📖 使用方法

```
用法: PDBonnie [OPTIONS] PDB_ID

  PDBonnie: a simple PDB structures downloader for bioinformatics research.

参数:
  PDB_ID              PDB ID，4 位字母数字组合（如 3COM）

选项:
  -f, --format TEXT   下载格式 (mmcif, pdb, xml, mmtf, bundle)，默认 mmcif
  -o, --output TEXT   保存路径，默认当前目录
  --obsolete          允许下载已废弃的结构
  --help              显示帮助信息
```

### 示例

```bash
# 下载默认 mmCIF 格式
PDBonnie 3COM

# 下载传统 PDB 格式
PDBonnie 3COM -f pdb

# 下载到指定目录
PDBonnie 3COM -o ./structures

# 下载 XML 格式
PDBonnie 1BNA -f xml

# 下载 MMTF 压缩格式
PDBonnie 4HHB -f mmtf

# 下载已废弃的结构
PDBonnie 1OLD --obsolete
```

### 输出示例

```
Downloading PDB structure '3com'...
Download completed in 1.28 s.
Structure saved in D:\PDBonnie\3com.cif
```


## 🔧 自行编译

如需自行编译为独立可执行文件，请使用 [Nuitka](https://nuitka.net/)：

```bash
pip install nuitka zstandard

python -m nuitka --onefile \
    --assume-yes-for-downloads \
    --lto=no \
    --output-filename=PDBonnie \
    main.py
```


## 🛠️ 技术栈

- [Python 3.12](https://www.python.org/) — 运行时
- [Biopython](https://biopython.org/) — PDB 结构下载
- [Click](https://click.palletsprojects.com/) — CLI 框架
- [Nuitka](https://nuitka.net/) — 编译为独立可执行文件
- [zstandard](https://github.com/facebook/zstd) — 可执行文件压缩


## 📝 许可证

MIT © 2025


## 🤝 致谢

- 蛋白质结构数据由 [RCSB PDB](https://www.rcsb.org/) 提供
- 下载功能基于 Biopython 的 `Bio.PDB.PDBList`
