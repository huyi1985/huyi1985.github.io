---
title: Linux给引入AI生成代码立规矩：可以用AI，但别想甩锅
date: '2026-04-13'
---

# Linux给引入AI生成代码立规矩：可以用AI，但别想甩锅

经过数月的激烈争论之后，Linus Torvalds 率 Linux 内核维护者终于就 **AI 生成代码的引入方式**达成一致，并正式确定了相关规则。

![](/assets/lwt3g4.webp)

长期以来，开源社区在“如何看待 AI 生成代码”这个问题上存在明显分歧：一边担心 AI 会带来质量问题和安全风险，主张限制甚至禁止使用；另一边则认为 AI 已经是现实中的开发工具，重点不在“能不能用”，而在“怎么用”。

这次 Linux 的选择明显偏向后者，也更**务实**。

本周，Linux 内核项目正式发布新政策：允许 AI 辅助生成代码进入内核开发流程，但前提是必须遵守清晰的责任归属规则——说白了，就是**出了问题谁来背锅要先说清楚**。

![](/assets/e8mngd.webp)

一份新增到 Linux 内核的文档 `Documentation/process/coding-assistants.rst`，对规则做了简单说明。核心要求是：AI 参与生成的代码不能使用具有法律意义的 `Signed-off-by` 标签，而要改用新的 `Assisted-by` 标签，用来标明所使用的 AI Agent、模型版本以及相关辅助工具，例如 `Assisted-by: Claude:claude-3-opus coccinelle sparse`。

更关键的是，不管代码是不是 AI 生成的，只要出了问题——包括 bug、安全漏洞等，**最终责任一律由提交代码的人类开发者承担**。

这套规则的出台，来自今年 1 月 Linux 内核邮件列表中的一轮激烈争论。当时 Intel 工程师 Dave Hansen 与 Oracle 工程师 Lorenzo Stoakes 围绕 AI 工具是否应该严格限制发生正面交锋，很快引发整个社区对“AI 是否应该进入内核开发流程”的分歧讨论。

最终 Linus Torvalds 以一贯直接了当的风格结束了争论。他认为，是否应全面禁止 AI 是“毫无意义的讨论”，问题的重点不在工具本身，而在责任归属。

有意思的是，Torvalds 在个人项目里就在使用 AI 辅助开发。他曾在一个名为 `AudioNoise` 的音频可视化工具项目中，让 AI 帮忙实现部分功能。在提交记录里，他提到内置的矩形选择工具不太好用，于是让 AI 写了一个自定义版本，并表示如果问他 AI 写的效果是不是比手写更好，答案是“当然更好”。

![合并进展基本顺利……在让 Antigravity 改成自定义的 RectangleSelector 之后，效果好多了](/assets/we74j1.png)

不过他也强调，这种用法只适用于个人项目；在 Linux 内核这种基础设施级别的工程里，标准必须更严格。

Torvalds 的观点再一次延续了 Linux 一贯的工程现实主义：AI 本质上只是工具，和编译器、静态分析工具没有本质区别。能写好代码的开发者，不会因为用了 AI 就变差；写不好代码的人，也不会因为禁止 AI 就变好。所以与其纠结工具本身，不如把规则定清楚，把责任直接锁定在提交者身上。

🔚

---

```
commit 93a72563cba609a414297b558cb46ddd3ce9d6b5
Merge: 4e52425 4e3eb84
Author: Linus Torvalds <torvalds@linux-foundation.org>
Date:   Wed Jan 7 14:38:39 2026 -0800

    Merge branch 'antigravity'
    
    This is Google Antigravity fixing up my visualization tool (which was
    also generated with help from google, but of the normal kind).
    
    It mostly went smoothly, although I had to figure out what the problem
    with using the builtin rectangle select was.  After telling antigravity
    to just do a custom RectangleSelector, things went much better.
    
    Is this much better than I could do by hand? Sure is.
```
