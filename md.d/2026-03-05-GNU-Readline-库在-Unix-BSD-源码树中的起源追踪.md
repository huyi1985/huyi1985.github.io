---
title: GNU Readline 库在 Unix/BSD 源码树中的起源追踪
date: '2026-03-05'
draft: true
---

# GNU Readline 库在 Unix/BSD 源码树中的起源追踪

## 研究方法

在 unix-history-repo 的所有分支中搜索 `readline` 相关文件，追踪其首次出现的时间、路径和上下文。

## 核心发现

**Readline 从未是 Unix/BSD 的原生组件**，它是 GNU 生态的产物，通过工具链依赖（GDB、bash）进入了 BSD 源码树。

## 时间线

| 日期 | 分支 | 事件 |
|------|------|------|
| **1987** | — | Brian Fox 为 GNU bash 编写 readline（版权标注年份） |
| **1989-06-28** | — | Brian Fox 将 readline 和 history 从 bash 中拆分为独立库（ChangeLog 最早记录） |
| **1989-09-19** | BSD 4.3 Net/2 | `readline.h` 首次出现在仓库中，随 GDB 捆绑进入 `usr/src/usr.bin/gdb/readline/` |
| **1991-05-08** | 386BSD 0.0 | `readline.c` 出现，SCCS 标记 `@(#)readline.c 6.4 (Berkeley) 5/8/91`，由 Donn Seeley (UUNET) 和 Van Jacobson (LBL) 修改 |
| **1992-06-23** | BSD-SCCS | BSD 自己的替代品 **libedit** 由 Christos Zoulas (Cornell) 贡献，进入 `usr/src/lib/libedit/` |
| **1992-10-14** | BSD 4.4 | GDB 4.7 带来更新版的 readline，路径 `usr/src/contrib/gdb-4.7.lbl/readline/` |
| **1994-05-09** | FreeBSD | Andrey Chernov 将 readline 抽出为独立共享库 `gnu/lib/libreadline/`，提交信息："Really we don't need copy of this library into each program (gdb f.e.)" |

## 仓库中最早的 readline 文件清单

分支：`BSD-4_3_Net_2-Snapshot-Development`
路径：`usr/src/usr.bin/gdb/readline/`

```
readline.c      (5557 行, Copyright 1987,1989 FSF)
readline.h
history.c       (Copyright 1989 FSF)
history.h
keymaps.c / keymaps.h
funmap.c
emacs_keymap.c
vi_keymap.c
vi_mode.c
chardefs.h
ChangeLog       (最早条目 1989-06-28 Brian Fox)
Makefile.gnu
```

## 源码版权

```c
/* readline.c -- a general facility for reading lines of input
   with emacs style editing and completion. */

/* Copyright (C) 1987,1989 Free Software Foundation, Inc. */
```

```c
/* History.c -- standalone history library */

/* Copyright (C) 1989 Free Software Foundation, Inc. */
```

## ChangeLog 摘要（最早条目）

```
Wed Jun 28 20:20:51 1989  Brian Fox  (bfox at aurel)
    * Made readline and history into independent libraries.

Tue Jul 11 06:25:01 1989  Brian Fox  (bfox at aurel)
    * readline.c: new variable rl_tilde_expander.
    * readline.h - new file chardefs.h (separates internal/public API)

Tue Aug  8 18:13:57 1989  Brian Fox  (bfox at aurel)
    * readline.c: Changed handling of EOF.
    * readline.c: Added support for event driven programs.

Fri Sep  8 09:00:45 1989  Brian Fox  (bfox at aurel)
    * readline.c: rl_prep_terminal(). Only turn on 8th bit
      as meta-bit iff the terminal is not using parity.

Sun Nov 26 16:29:11 1989  Jim Kingdon  (kingdon at hobbes.ai.mit.edu)
    * readline.c: rl_deprep_terminal - restore local_mode_flags fix

Thu Feb  8 01:04:00 1990  Jim Kingdon  (kingdon at pogo.ai.mit.edu)
    * Makefile: Uncomment out ranlib line.
```

## BSD 的回应：libedit（1992）

由于 readline 使用 GPL 许可，BSD 阵营在 1992 年创建了 BSD 许可的替代品：

```c
/* Copyright (c) 1992, 1993
 *    The Regents of the University of California.  All rights reserved.
 *
 * This code is derived from software contributed to Berkeley by
 * Christos Zoulas of Cornell University. */
```

- 路径：`usr/src/lib/libedit/`
- 首次提交：1992-06-23 by bostic
- 提供 readline 兼容 API，BSD 许可
- FreeBSD base system 至今使用 libedit 而非 readline

## 两者对比

| 属性 | GNU Readline | BSD libedit |
|------|-------------|-------------|
| 作者 | Brian Fox (FSF) | Christos Zoulas (Cornell/Berkeley) |
| 原创年份 | 1987 | 1992 |
| 许可 | GPL | BSD |
| 仓库首现 | 1989 (BSD 4.3 Net/2, 随 GDB) | 1992 (BSD-SCCS, 原生库) |
| 进入方式 | 第三方工具依赖 | BSD 原生开发 |
| FreeBSD 中 | ports/packages 安装 | base system 内置 |

## 关键洞察

1. readline 通过 GDB 这个 GNU 工具"搭便车"进入了 BSD 源码树，而非被 BSD 主动引入
2. GPL 许可是 BSD 阵营开发 libedit 替代品的直接原因
3. 1994 年 FreeBSD 的 Andrey Chernov 首次将 readline 从 GDB 子目录中提取为独立共享库
4. Brian Fox 1989 年将 readline 从 bash 中拆分为独立库是关键转折点，使其能被其他 GNU 工具（GDB）采用

## 附录：GNU 出过操作系统吗？

GNU（GNU's Not Unix）从未发布过完整的操作系统。

### GNU 项目的工具链时间线

1983 年 Richard Stallman 在 MIT AI Lab 发起 GNU 项目，目标是创建一个完全自由的 Unix 兼容操作系统。采用自上而下的开发策略——先做用户态工具，最后做内核：

| 时间 | 组件 | 状态 |
|------|------|------|
| 1984 | Emacs | 完成 |
| 1987 | GCC | 完成 |
| 1986 | GDB | 完成 |
| 1989 | bash (Brian Fox) | 完成 |
| 1989 | readline | 完成 |
| 1986-89 | coreutils (ls, cp, cat...) | 完成 |
| 1990 | **GNU Hurd**（内核） | **至今未完成** |

### GNU Hurd —— 永远的"明年完成"

GNU 计划的内核叫 Hurd，基于 Mach 微内核架构。Stallman 选择微内核是因为当时认为它比宏内核更先进，但微内核的复杂性远超预期，Hurd 的开发陷入了长期停滞。

1991 年 Linus Torvalds 发布了 Linux 内核（宏内核）。Linux 内核 + GNU 用户态工具 = 人们通常说的 "Linux"，Stallman 坚持称其为 "GNU/Linux"。

Hurd 至今仍在开发中，Debian 有实验性的 Debian GNU/Hurd 发行版，但从未达到生产可用状态。

### 在 unix-history-repo 中的 GNU 组件痕迹

GNU 的工具通过依赖关系渗透进了 BSD 源码树，在仓库中可见的 GNU 组件包括：

- **GDB**（含 readline）— BSD 4.3 Net/2 起
- **GCC** — BSD 后期和 FreeBSD
- **groff** — BSD 4.3 Net/2 中有 `usr/src/usr.bin/groff/`
- **bash** — FreeBSD ports

这些都是工具，不是操作系统。GNU 的讽刺之处在于：它为一个从未完成的操作系统造出了世界上最成功的工具链，而这些工具最终跑在了别人的内核（Linux）和别人的系统（BSD）上。
