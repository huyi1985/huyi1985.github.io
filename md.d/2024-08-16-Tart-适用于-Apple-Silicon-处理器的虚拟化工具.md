---
title: Tart——适用于 Apple Silicon 处理器的虚拟化工具
date: '2024-08-16'
---

前一阵，单位好不容易“开恩”，给我把使用了多年的 Intel MacBook 换成了 M3 的 MacBook。

新电脑好是好，但我常用的虚拟机软件 VirtualBox 却不兼容 M3 处理器，

![[Pasted image 20240816175004.png]]

哎～只好先用 Docker 代替了。

这两天，突然发现一款名为 *Tart* 的虚拟化工具竟然可以轻松在 M3 的 MacBook 上安装虚拟机。

*Tart* 是专门针对 Apple Silicon 处理器的虚拟化工具，它工作在 Apple Silicon 的原生虚拟化框架上，因此可以高速运行 macOS 和 Linux 的虚拟机。

使用下面的 `brew` 命令安装好 *Tart* 后，就可以通过 `tart` 命令管理虚拟机了。

```bash
$ brew install cirruslabs/cli/tart
```

先来创建一个 *Ubuntu* 的虚拟机玩玩：



你也来试试呗，*Tart* 的虚拟机还是挺好用的。