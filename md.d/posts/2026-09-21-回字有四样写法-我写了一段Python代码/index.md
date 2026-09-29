---
title: “回字有四样写法”，我写了一段Python代码
date: '2026-09-18'
tags:
- 文件
- man
- Python
- 代码
- code
- 数据库
- 数据
---

# “回字有四样写法”，我写了一段Python代码

“孔乙己显出极高兴的样子，将两个指头的长指甲敲着柜台，点头说，“对呀对呀！……回字有四样写法，你知道么？……”

于是，我写了一段 Python 代码，去问 Unicode 要答案。

Unicode 为汉字专门建了一个数据库，叫 Unihan（Unicode Han Database），里面有个叫 Unihan_Variants.txt 的文件，用于记录异体字，每行三列。

只要找到第 1 列为“回”字码点 U+56DE；第 2 列为 kSemanticVariant（表示意思完全一样的异体字）的那一行，就能翻出“回”字另外 3 种写法：囘 (U+56D8)、廻 (U+5EFB)、囬 (U+56EC)。
