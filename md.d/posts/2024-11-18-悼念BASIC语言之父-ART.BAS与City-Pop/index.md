---
title: 悼念BASIC语言之父：ART.BAS与City Pop
date: '2024-11-18'
---

# 悼念BASIC语言之父：ART.BAS与City Pop

**2024 年 11 月 12 日，BASIC 语言的发明者之一 Thomas E. Kurtz 教授与世长辞，享年 96 岁**。

![](img1.jpg)

> BASIC 语言的两位发明者：John Kemeny (图左) 和 Thomas Kurtz (图右)

消息传出后，在 Hacker News 等技术社区，无数程序员自发分享起他们与 BASIC 的故事，

```BASIC
10 PRINT "WE REMEMBER KURTZ"
20 GOTO 10
```

![](img2.png)

本文讲述了 1980 年代初 BASIC 代码与艺术的一次融合——ART.BAS 与 City Pop，以此来深切悼念 Thomas E. Kurtz。

---

1981 年 8 月，IBM 和 微软公司联手，推出了第一台 IBM PC（IBM 5150）。微软公司使用 BASIC 为这款划时代的个人计算机编写了多个演示程序，以呈现其性能。这当中就有一个名为 **ART.BAS** 的 BASIC 程序。

光凭 ART 这个名字就能猜出这是一个**计算机技术和艺术结合的作品**，下面我们就来重现这个昔日的成果。

![art.bas](img3.gif)

> 大家可以通过 https://www.pcjs.org/software/pcx86/app/ibm/BASIC/1.00/ 这个网页体验。体验方法：
> 1. 待屏幕上出现 `A>`
> 2. 输入 `basica art.bas`，按下回车键
> 3. 待出现 "ART Version 1.00" 后，按下空格键

既然这幅作品名为“The City”，那么这些**随机出现的矩形**应该就是要表现都市的繁荣发展。看！那变幻莫测的天际线！

（不过，要没刷过 LeetCode 上“天际线”那题，我是真看不出来这是要表现高楼大厦）

```bas
1410 IX1=RND*250+35
1420 IX2=RND*250+35
1430 IX2 = (IX1-IX2)/3 + IX2
1440 IY1=RND*110+55
1450 IY2=165
1460 LINE (IX1,IY1)-(IX2,IY2),RND*2+1,BF
1470 LINE (IX1,IY1)-(IX2,IY2),0,B
1480 LINE (IX1+1,IY1+1)-(IX2-1,IY2-1),0,B
...
```

---

说到快速发展的城市，有一种称为 **City Pop** 的音乐风格敏锐地捕捉到了这种现象。

**City Pop** 起源于 **20 世纪 70 年代末到 80 年代**的日本，反映了当时日本快速发展的都市生活和经济繁荣，充满了现代、时尚和富有都市感的气息。

City Pop 将流行、摇滚、放克、爵士、迪斯科和 R&B 等多种风格融合在一起，这种混搭让 City Pop 拥有丰富的音乐层次感。很多歌曲会让人联想到驾车兜风、海滩度假和都市夜晚的霓虹灯。

ART.BAS 这段程序的背景音乐是通过如下代码随机生成的，只有嗡嗡声。但若把 City Pop 和 ART.BAS 的画面结合起来……

```BASIC
1410 IX1=RND*250+35
1420 IX2=RND*250+35
1430 IX2 = (IX1-IX2)/3 + IX2
1440 IY1=RND*110+55
1450 IY2=165
...
1490 IA = ABS((IX1-IX2)*(IY1-IY2))
1500 IS = (36400!-IA)/360 + 37
1510 SOUND IS,2
```

艺术已成，请欣赏！



另外，比尔盖茨还亲自使用 BASIC 为 IBM PC 编写过一款游戏，请阅读《比尔·盖茨、驴子🫏与IBM》。
