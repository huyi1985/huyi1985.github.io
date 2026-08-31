---
title: 在1982年相距上千公里的两台计算机之间是如何传输文件的
date: '2025-07-21'
---

# 在1982年相距上千公里的两台计算机之间是如何传输文件的

https://zh.wikipedia.org/wiki/%E9%98%BF%E5%B8%83%E5%93%88%E6%A1%91%C2%B7%E5%B7%B4%E5%B0%BC%E8%90%A8%E5%BE%B7%E5%B0%94 阿布哈桑·巴尼萨德尔

https://ia801605.us.archive.org/24/items/kilobaudmagazine-1982-07/Microcomputing_1982_July.pdf

跨大西洋通信的案例

民用互联网 Web 电话网络 + 电报网络


> 今天，爷爷奶奶都能和小孙子孙女之间相互发送照片和视频

David Kline 是美国伊利诺伊州 Impact Features 的总监，这是一家为自由撰稿人服务的机构。他曾在 1980 年代，受哥伦比亚广播公司电视台、洛杉矶时报和芝加哥太阳时报的委托，前往阿富汗开展报道。

> 在其他记者和撰稿人还在使用电传打字机，David 就尝试使用 Osborne + 调制解调器 传输文件
> 委托海外的打字员——只能用英语写稿件，而且

> 使用 世界上第一台便携式计算机 Osborne + 软件 **MODEM7** + 调制解调器，跨越大西洋，将稿件传输到了上千公里之外的远程计算机上。

> Osborne 是世界上第一台……

> XModem BBS 的创始人……

> 调制解调器 和 声学耦合器

促成这次跨越上千公里的文件传输的契机是，David 被派去巴黎采访流亡的伊朗总统阿布哈桑·巴尼萨德尔（Abolhassan Banisadr）。这次采访让 David 第一次有机会在美国之外测试 Osborne 加调制解调器，看看能否通过远距离电话线准确地传输文章。

在此次意义非凡的试验中，David 有一位得力助手 Marty。Marty Cawthorn 就职于美国密歇根州 Cawthorn Scientific Group 公司，该公司专门从事计算机通信以及定制软件的开发。Marty 不仅是 David 的技术支持，还充当他与各家报社之间的中转站。二人的计划是 Marty 先通过 **MODEM7** 文件传输程序接收 David 的文章，然后再将文章短距离重新传输到各家报社。

到达巴黎后，David 立即开展了采访工作。采访过后，David 回到酒店，便开始埋头撰写报道。晚上 7 点，David 准备打电话给 Marty，开始他们突破性的试验——跨越大西洋传输文件。

可就在这时，David 却犹豫起来。因为他刚刚注意到，法国电话的话机（handset）（由话筒和听筒组成的部分）与美国的略有不同，法国的是方形的而不是圆形的。如果方形的话机不能紧贴调制解调器，无法产生足够强的信号，导致调制解调器不能用怎么办？

就算 Osborne 和调制解调器能正常运行，但还有一个更棘手的问题：法国电话运营商会不会监听到有人不是正常通话，而在使用电话线传输数据，进而报告情报机构第二局（Deuxième Bureau），以间谍罪逮捕他？

最终 David 还是鼓起勇气下定决心，给 Marty 拨通了电话。

---

David 在《文章》中记录了这次文件传输的过程。下面我们就一起重温这一激动人心的时刻：

> David 只是描述了屏幕上的内容。
> 对照着 XModem 的汇编代码，尽可能还原当时屏幕上的内容

Marty 一接电话，我就将调制解调器（modem）设置为发起模式，他则将他的调制解调器设置为应答模式。当从电话听筒听到载波音后，我就将听筒猛地塞进（slam）调制解调器（大力出奇迹，方头也能塞进圆形的？），并输入发送文件的命令：

```
S B: Banisadr.Int
```

按下回车键后，我就死死盯住屏幕。屏幕上显示出

```
File Open, size 78 Sectors
Awaiting Initial NAK
```

过了 1 秒钟，Marty 的电脑却没有响应。又过了 1 秒钟，仍然没有响应。我紧张得直冒汗，然而屏幕上却是一遍又一遍冷漠地重复着“Awaiting Initial NAK”，仿佛生怕我错过了这一重要消息似的。


突然，我听到了 Osborne 的磁盘驱动器发出了悦耳的声音——实际上却吵得像窗外的啄木鸟。这说明 Marty 的电脑开始接收数据了！第 1 个 Section 发送出去了，随后是第 2 个，第 3 个……

但在发送第 48 个 Section 时，出问题了。屏幕上显示

```
H RCD
```

“啊？没有 ACK！”我喊道。

然而，就在我真正陷入疯狂之前，问题自己解决了！可能只是跨洋电话线路中的噪音激增。


"Send Sector #49," the Osborne began again, this time (or so it seemed to me) in a tone of disapproval over my obvious emotional instability. And so it went, all the way up to "Send Sector #78." Then came, finally, "All Transfers Completed!"

“发送扇区 #49”……一直到“发送扇区 #78”。最后，“所有传输完成！”

我成功地从巴黎完成了计算，毕竟，巴黎是现代科技世界的中心。

> 前方阿富汗，在法国同行骂骂咧咧的抱怨声中，收工回家

---

https://ia600103.us.archive.org/13/items/byte-magazine-1983-07-rescan/1983_07_BYTE_08-07_Videotex.pdf

https://ia801605.us.archive.org/24/items/kilobaudmagazine-1982-07/Microcomputing_1982_July.pdf

%%

As soon as Marty answered, I set my modem to originate; he set his to answer. When I heard his carrier tone, I slammed my receiver down into the modem and punched out the command for sending a file: S B: Banisadr.Int. 

Then I hit the return key and watched the machine go to work:

"File Open, size 78 Sectors," declared my computer screen. Nonchalantly, it added that it was "Awaiting Initial NAK."

Finally, I heard those lovely grating sounds of the Osborne disk drives in action— something like a flatulent woodpecker, actually— and I knew the acknowledgement was received. The damn thing was working! First it sent Sector #1, then Sector #2 and on and on it kept on going!

Then I noticed something amiss at Sector #48:

"H RCD," smirked my Osborne. "Not ACK."

"Not ACK?!" I shouted back. Before I could really work myself into a frenzy, however, the problem resolved itself, whatever it was. Probably just a spike of noise in the overseas phone call.

OK, so I successfully computed from Paris, a city, after all, that is very much at the center of our modern technological world. The real challenge lay ahead. It still remained to be seen whether I'd be able to use a computer as a reporter's tool from the legendary Land of the Khyber, where life has haid\y changed at all in the 25 centuries since Alexander the Great's conquering spearmen first met and fought the fierce Afghan tribes in battle.
%%