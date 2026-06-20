# Changelog

所有值得注意的项目变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。

## [Unreleased]

## [1.0.0] - 2025-XX-XX

### Added

- 初始版本发布
- 支持通过 PDB ID 下载蛋白质结构
- 支持五种下载格式：mmCIF、PDB、XML、MMTF、Bundle
- 30 秒下载超时保护
- PDB ID 格式校验（正则匹配 `[A-Z0-9]{4}`）
- 自定义输出目录支持
- 支持下载已废弃（obsolete）结构
- 提供 Nuitka 编译的 Windows 单文件可执行程序
- 自动显示下载耗时与保存路径