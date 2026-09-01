---
title: 操作系统能知道自己是在虚拟机中运行的吗？
date: '2024-12-13'
tags:
- Linux
- 操作系统
- bash
- 命令
- 指令
- 文件
- 文件系统
- 路径
- 输出
- man
- 信号
- signal
- DEC
- Go
- CPU
- 计算机
- x86
- nc
- vi
- 数据
- AI
- 苹果
- Mac
- macOS
- 软件
---

# 操作系统能知道自己是在虚拟机中运行的吗？

“这是最后的机会，之后你将无法回头。服下**蓝药丸**，故事结束，你会在床上醒来，继续信任你愿意相信的一切。服下**红药丸**，你将留在仙境，我会带你走进兔子洞，告诉你真相有多深……记住，我所提供的，只有真相，仅此而已……”

> This is your last chance. After this there is no turning back. You take the ***blue pill***, the story ends, you wake up in your bed and believe whatever you want to believe. You take the ***red pill***, you stay in *Wonderland*, and I show you how deep the *rabbit hole* goes… Remember, all I’m offering is the truth, nothing more…

这是电影《黑客帝国1》中的经典场景之一。墨菲斯（Morpheus）邀请尼奥（Neo）做出一个决定，选择红药丸还是蓝药丸——选择追求真相还是沉迷虚假。

![](img1.png)

运行在虚拟机中的操作系统与生活（被奴役）在矩阵中的居民面临同样的问题，它们能够感知到自己运行在一个虚幻的环境中吗？或者说，它们能够区分自己是运行在真正的硬件上，还是由 **Oracle** VirtualBox、VMware 等虚拟机软件创建的“矩阵”中呢？

> 真巧，Oracle（先知）一词出现在了一篇以黑客帝国开场的文章中

答案是**取决于具体情况，但有些线索能够帮助操作系统判断身在何处**。

---

例如，这里在苹果的 macOS 上安装了 Oracle VirtualBox，又在新建的虚拟机中安装了 Ubuntu。那 Ubuntu 是否知道自己运行在虚拟机，而不是 mac 中呢？

只需要在 Ubuntu 中执行一条命令就可以知道答案：

```bash
$ systemd-detect-virt
oracle
```

![](img2.png)

这里输出了“oracle”，证明 **Ubuntu 是知道自己运行在 Oracle VirtualBox 中的**。

该命令的工作原理其实不难：通过一系列预设的探索策略，检查运行在虚拟机中的操作系统的“隐秘角落”，寻找真相。

比如，最简单的策略之一就是扫描如下文件：

* /sys/class/dmi/id/product_name
* /sys/class/dmi/id/sys_vendor
* /sys/class/dmi/id/board_vendor
* /sys/class/dmi/id/bios_vendor
* /sys/class/dmi/id/product_version

若在其中发现 `VirtualBox`、`VMware`、`Amazon EC2`、`QEMU` 等关键词，就可以知道自己是运行在对应的虚拟机中。

> `/sys/class/dmi` 是什么
> 
>在 Linux 系统中，`/sys/class/dmi` 是一个虚拟文件系统路径（执行 `mount` 命令可以看到，`sysfs on /sys type sysfs (rw,noexec,nosuid,nodev)`），用于访问有关硬件系统的信息，尤其是与 DMI（Desktop Management Interface）相关的数据。
>
>DMI 是一种用于在计算机系统中管理硬件的信息接口，提供系统厂商（`sys_vendor`）、主板（`board_vendor`）、BIOS（`bios_vendor`）等详细信息。

![](img3.png)

`systemd-detect-virt` 命令的其他策略还包括探索 `/proc/device-tree/`、`/sys/hypervisor/` 等路径的内容。当无法从这些特殊的文件中找到有价值的信息时，该命令还会执行 x86 架构 CPU 中的一条特殊指令 `CPUID`，以此来获取虚拟环境的信息。

此外，该命令还能判断操作系统是否运行在 Docker、LXC 等容器中。

除了 `systemd-detect-virt` 命令，`hostnamectl` 命令也能输出有关操作系统运行环境的信息。

![](img4.png)

---

![](img5.png)

尼奥选择了红药丸，随后墨菲斯告知尼奥现在差不多是 2199 年，而不是他以为的 1999 年。这时，墨菲斯提出了一个核心问题，**什么是真实**？

“什么才是真实？你怎么定义‘真实’？如果你说的‘真实’是你能触摸到的、能闻到的、能品尝到的、能看到的，那‘真实’其实就是你大脑解读的电信号。”

> What is ***real***? How do you define real? If you’re talking about what you can feel, what you can smell, what you can taste and see, then *real is simply electrical signals interpreted by your brain*. 

正如墨菲斯所说，你认为眼见为实，`systemd-detect-virt` 也是这样“想”的，它会优先根据从 `/sys/class/dmi/id/`中看到的内容为判断依据，接收来自此处的信号。

那我是不是能通过篡改这些文件，从而让操作系统误以为运行在另一个虚拟空间中呢？理论上是可以的，只不过看看那些文件的权限。

```bash
-r--r--r-- 1 root root 4096 Dec  4 19:11 /sys/class/dmi/id/bios_vendor
-r--r--r-- 1 root root 4096 Dec  4 19:11 /sys/class/dmi/id/board_vendor
-r--r--r-- 1 root root 4096 Dec  4 19:13 /sys/class/dmi/id/chassis_vendor
-r--r--r-- 1 root root 4096 Dec  4 18:45 /sys/class/dmi/id/sys_vendor
...
```

“矩阵”不想让你醒来。
