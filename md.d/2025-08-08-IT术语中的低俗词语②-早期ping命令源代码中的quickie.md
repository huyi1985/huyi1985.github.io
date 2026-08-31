---
title: IT术语中的低俗词语②：早期ping命令源代码中的quickie
date: '2025-08-08'
---

# IT术语中的低俗词语②：早期ping命令源代码中的quickie

IT 术语（黑话）自有其传承。早期黑客文化中，讽刺与反叛几乎是一种身份象征，不正经，才够格。调侃、低俗乃至粗口风格的俚语成为黑客社群的通用术语，其中一些词语还沉淀到了官方文档和源代码中。

今天要和大家分享的**低俗 IT 术语**是“**quickie**”，出自**早期 ping 命令的源代码**。

![](/assets/gt5ni5.webp)

## 一夜之间，ping 诞生了

1983 年年底，就职于美国弹道研究实验室的 **Mike Muuss** 时年 25 岁，为了解决工作中烦人的网络问题，他熬了个通宵编写出了千行左右的代码。**一夜之间 ping 命令诞生了**。

![Michael John Muuss 1958 年 10 月 16 日～2000 年 11 月 20 日](/assets/a7fkp8.webp)

那一晚，Muuss 不仅用 C 语言编写了 500 行左右的代码，做出了 ping 命令，还顺带修改了操作系统 BSD Unix 4.2a 的内核。因为他发现虽然代码能顺利通过编译，但程序的行为却不符合预期，查来查去是内核不支持 **ICMP 原始套接字**（raw socket）导致的，而这正是 ping 所依赖的基础功能。

Muuss 为 ping 命令设置了几种工作模式，有每隔 1 秒就发送 1 个 `ICMP_ECHO` 数据包的默认模式，有一刻不停疯狂发送数据包的洪水（flood）模式，还有这两种模式的结合体：先不管三七二十一发出去几个数据包看看，再进入平和的默认模式，这样一股脑儿发送的数据包叫作 **preload**。

在发送 preload 数据包时，Muuss 写下了这样的注释：

![](/assets/f87x2l.png)

“**fire off them quickies**”！网络出问题了，管它什么原因呢，先发射几个 `ICMP_ECHO` 数据包出去看看。

## 一夜成名，ping 成了系统标配

第二天，Muuss 兴冲冲来到办公室，打算用奋战一夜的成果 ping 命令来分析烦人的网络问题。但就在他熬夜编写代码的时候，一位同事竟把问题解决了。虽然 ping 失去了首秀的机会，但 BSD Unix 的维护者，加州大学伯克利分校的人察觉到了 ping 的价值，迫不及待地要走了 Muuss 修改后的内核代码和 ping 的源代码。

随后，ping 就成了 BSD Unix 的标准组件。不久后，ping 又被移植到了其他的操作系统中。而今天，无论是 Windows、Linux 还是 macOS，在任何主流的操作系统上几乎都可以使用 ping 命令来测试网络通不通，网速快不快。

成为了标配的 ping 也“文明”了起来，在使用手册（`man ping`）中，用于发送 preload 的 `-l` 选项的说明是：

> *-l preload*
> If preload is specified, ping sends that many packets **as fast as possible** before falling into its normal mode of behavior. Only the super-user may use this option.

“**quickies**”改成了中规中矩的“**as fast as possible**”。

---

说点题外话吧。我曾在一条小街里的写字楼上工作过。每次加班到深夜，街道两侧的大多数店铺早已关门，只剩街角一间小店还亮着粉灯，还有旁边那家名叫“**快客**”的便利店在营业。

🔚

![](/assets/2fs7a1.png)

📖 推荐阅读

![](/assets/gfrh0r.png)

---
## ping.c
```c
	/* fire off them quickies */
	for(i=0; i < preload; i++)
		pinger();

// quickie
// ① (drink) 两三口喝下的酒
// ② (sexual act) 瞬间完事的性交
```