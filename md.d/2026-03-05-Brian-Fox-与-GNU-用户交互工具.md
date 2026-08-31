---
title: Brian Fox 与 GNU 用户交互工具
date: '2026-03-05'
---

# Brian Fox 与 GNU 用户交互工具

## Brian Fox 的三大贡献

Brian Fox 对 GNU 用户交互层面的贡献集中在三件事——都是人和系统之间的界面：

| 工具 | 年份 | 作用 |
|------|------|------|
| **bash** | 1989 | 交互式 shell，替代 Bourne shell |
| **readline** | 1987 编写，1989 独立 | 行编辑库，提供 Emacs/vi 风格的输入编辑和补全 |
| **info** | ~1989 | 独立的 Texinfo 文档阅读器，不依赖 Emacs |

## GNU Info 程序

### 它做什么

在万维网（WWW）出现之前（1989 年 Berners-Lee 才提出 Web），Info 就实现了超文本导航——文档被组织成节点（node）构成的树状结构，用户可以通过交叉引用链接在节点之间跳转。

与 man 页面的对比：

| 特性 | man | info |
|------|-----|------|
| 结构 | 线性、单页 | 树状、多节点 |
| 导航 | 顺序滚动 | 超链接跳转、菜单 |
| 索引 | 无 | 支持 |
| 交叉引用 | SEE ALSO 文字 | 可跳转的链接 |
| 格式 | troff/nroff | Texinfo |

GNU 的所有工具（gcc、gdb、bash、coreutils...）都用 Texinfo 写文档，用 `info` 命令阅读。

### Texinfo 格式 vs info 阅读器

| 组件 | 作者 | 说明 |
|------|------|------|
| **Texinfo 格式** | Richard Stallman | 文档标记语言，Emacs 内置有 Info 阅读模式（`C-h i`） |
| **独立 `info` 程序** | Brian Fox | 终端下的独立阅读器，不依赖 Emacs |

Stallman 最初设计 Texinfo 时，只能在 Emacs 里阅读 Info 文档。Brian Fox 写了独立命令行 `info` 程序，让所有用户都能方便地阅读 GNU 文档。

## 在 unix-history-repo 中的痕迹

- **readline** — 随 GDB 进入 BSD 4.3 Net/2（1989），见 `usr/src/usr.bin/gdb/readline/`
- **Texinfo 文档** — BSD 4.3 Net/2 的 GDB 中包含 `inc-readline.texinfo`、`readline.texinfo` 等 Info 格式文档
- **bash** — 通过 FreeBSD ports 系统提供
