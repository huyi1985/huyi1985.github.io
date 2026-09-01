---
title: History
date: '2025-06-17'
---

有人曾问 Ken Thompson：“如果能重来一次，你会怎么重新设计 UNIX？”  
他笑着说：“我会把 `creat` 拼成带 e 的 `create`。”

这个名字中缺了一个字母的系统调用，其实诞生于一次非常“极客”式的尝试。

时间回到 1968 年，Ken 和 Dennis 在实验室的一角发现了一台几乎被遗忘的 PDP-7 小型机。他们将自制的游戏 🎮 **Space Travel** 搬到了这台“裸机”上运行。

游戏跑起来后，Ken 借此机会动手实现了他早年在 MULTICS 项目中设计的一个理论文件系统。但系统不能只有文件系统，他们很快又写了第一个命令解释器（也就是 shell）和一套基础工具，能对文件进行创建、删除、复制等操作。

这一切，正是 UNIX 的雏形。而那个至今仍在 Stack Overflow 等技术论坛上频繁被问起的 `creat` 系统调用，就是在这段代码中诞生的。

图中展示的，是当年 `creat` 函数的汇编代码片段👇

https://archive.computerhistory.org/resources/access/text/2019/09/102785108-05-001-acc.pdf P43

### 🕰 The Origins of UNIX

**The year was 1968.**  

Ken Thompson and his colleagues in the Computer Research Group at Bell Labs had contributed significantly to the MULTICS project — a visionary computing environment. However, MULTICS had taken a wrong evolutionary turn. While it offered sophisticated features, it required substantial computing power. Its production versions proved too large and too slow, and the original design had to be scaled back during implementation.

Still, several working versions of MULTICS were completed, providing a pleasant computing environment. In contrast, Bell Labs’ alternative — a GE 645 emulating a GE 635 — was primarily batch-oriented, awkward, and unfriendly, despite its timesharing support.

Ken Thompson, along with Dennis Ritchie and Joseph Ossanna, didn’t want to lose the comfort MULTICS had provided. They began lobbying management for an **interactive time-sharing machine**, like the newly introduced **DEC-10**, on which they could build their own system. The DEC-10 was powerful and came with an impressive interactive environment — but it was **very expensive**.

**时间是 1968 年。**

Ken Thompson 和贝尔实验室计算机研究组的同事们在 MULTICS 项目中做出了重要贡献。MULTICS 是一个富有远见的计算环境，但它在发展过程中走上了一条错误的进化路线。虽然提供了非常先进的功能，却对计算资源的需求极为庞大。其最终的产品版本体积庞大、运行缓慢，原始设计也不得不在实现过程中进行大幅度的缩减。

尽管如此，MULTICS 的几个可用版本仍然被完成，并提供了令人愉快的使用体验。相比之下，贝尔实验室的替代方案——一台模拟 GE 635 的 GE 645 系统——虽然支持分时操作，但本质上还是以批处理为主，使用体验笨拙且不友好。

Ken Thompson 与 Dennis Ritchie、Joseph Ossanna 一起，不愿放弃 MULTICS 所带来的舒适环境，于是他们开始游说管理层，希望能获得一台**交互式分时系统**，例如刚推出不久的 **DEC-10**，作为平台来开发他们自己的操作系统。DEC-10 功能强大，配有出色的交互式分时环境——但价格也**非常昂贵**。

---

### ❌ Management Says No (Repeatedly)

Ken’s request for a DEC-10 was **repeatedly rejected**. Management, disillusioned by MULTICS’ failure, was unwilling to fund another OS project that felt like “MULTICS on different hardware.”

At the same time, Ken was working on a program called **Space Travel**, which simulated the movement of celestial bodies and a spaceship landing on planets. Though he installed it on the GE system, he found its performance unsatisfactory and the cost exorbitant — reportedly **$75 per game**, according to Dennis.

Luckily, Ken and Dennis discovered a **little-used PDP-7** sitting in a corner. Using the GE system, they created a **paper-tape executable** of Space Travel to run on the PDP-7’s bare hardware.


Ken 多次提出采购 DEC-10 的请求，却被**反复拒绝**。管理层因为对 MULTICS 项目的失败感到失望，无意再为另一个看起来像是“换了硬件的 MULTICS”操作系统项目提供资金支持。

与此同时，Ken 正在开发一个名为 **Space Travel** 的程序，它模拟了太阳系天体的运动，还可以操控飞船在不同星球上着陆。他曾将该程序安装到 GE 系统上运行，但发现性能非常差，运行起来也十分昂贵——据 Dennis 所说，一局游戏的成本竟然高达 **75 美元**。

幸运的是，Ken 和 Dennis 在角落里发现了一台**几乎没人使用的 PDP-7**。他们利用 GE 系统创建了一个 **纸带格式的可执行文件**，将 Space Travel 搬到了这台 PDP-7 的裸机上运行。

---

### 💾 In the Beginning...

With Space Travel running, Ken had a reason to implement the theoretical file system he had designed during the MULTICS project. Naturally, a full system required more — so the team wrote the first **command interpreter (shell)** and simple **file manipulation utilities**. Initially, they cross-compiled code from the GE to the PDP-7. Once an assembler was ready, the system became **self-hosting**.

This early system already had many **UNIX-like features**, including:

- `fork()` for multiprocessing
- A file system with **i-nodes**
- Special file types for directories and devices
- Support for **two users simultaneously**

### 💾 从头开始……

随着 Space Travel 成功运行，Ken 终于有了一个动机来实现他在 MULTICS 项目中曾经设计过的**理论文件系统**。当然，仅有文件系统还不够，于是团队又编写了第一个**命令解释器（shell）**以及一些用于**文件操作的简单工具**。最初，他们通过 GE 系统将代码交叉编译到 PDP-7 上；当汇编器开发完成后，整个系统便实现了**自举（self-hosting）**。

这一早期系统已经具备了许多**UNIX 的原型特征**，包括：

- 用于多进程支持的 `fork()`
- 使用 **i-node（索引节点）** 的文件系统
- 用于目录与设备的特殊文件类型
- 支持**两个用户同时使用**

---

### 🧩 From MULTICS to UNIX

MULTICS stood for **MULTiplexed Information and Computing System**. In 1970, Brian Kernighan jokingly dubbed their two-user version **“UNICS”** — **UNiplexed Information and Computing System** — as a light-hearted jab at the bloated MULTICS. (Some joked MULTICS meant “Many Unnecessarily Large Tables In Core Simultaneously.”)

Eventually, "UNICS" became simply **"UNIX"**, and the name stuck.

MULTICS 的全称是 MULTiplexed Information and Computing System（多路复用信息与计算系统）。1970 年，Brian Kernighan 开玩笑地将他们的两用户版本戏称为 “UNICS”——即 UNiplexed Information and Computing System（单路复用信息与计算系统），以此轻松调侃 MULTICS 的臃肿。（还有人笑称 MULTICS 是 “Many Unnecessarily Large Tables In Core Simultaneously” 的缩写，即“内存中同时存在许多不必要的大表”。）

最终，“UNICS” 被简化为 “UNIX”，这个名字也就这样流传了下来。

---

### 💡 The First UNIX Machine

The PDP-7 was **borrowed** and **underpowered**. The team submitted another proposal, this time for a **PDP-11/20**, with the concrete goal of researching **text processing**. Unlike the DEC-10, the PDP-11 was much cheaper. Management approved it.

In **1970**, UNIX was ported to the PDP-11/20 — a significant effort, as the system was entirely written in assembler. Tools like `roff` (a forerunner to `troff`) and a text editor were ported over, making the machine a legitimate **text-processing system**.

Coincidentally, the **Bell Labs patent office** was looking for such a system and chose the PDP-11/20 UNIX machine over commercial alternatives — making them the **first official UNIX users**.

💡 第一台 UNIX 机器
PDP-7 是一台借来的机器，而且性能有限。于是团队提交了另一份提案，这次是为了采购一台 PDP-11/20，并明确表示用途是用于研究文本处理。与 DEC-10 相比，PDP-11 便宜得多。管理层最终批准了这项采购。

在 1970 年，UNIX 被移植到了 PDP-11/20 上——这是一项不小的工程，因为整个系统都是用汇编语言编写的。像 roff（troff 的前身）和一个文本编辑器等工具也被移植到了新机器上，从而使这台机器成为一个名副其实的文本处理系统。

恰好当时 贝尔实验室的专利办公室正在寻找这样一个系统，最终他们选择了基于 PDP-11/20 的 UNIX 机器，而不是商业方案——这使他们成为了第一个正式的 UNIX 用户。
