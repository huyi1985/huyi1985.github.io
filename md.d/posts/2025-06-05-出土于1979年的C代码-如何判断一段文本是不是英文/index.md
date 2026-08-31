---
title: 出土于1979年的C代码：如何判断一段文本是不是英文？
date: '2025-06-05'
---

# 出土于1979年的C代码：如何判断一段文本是不是英文？
这段出土的 C 语言代码创作于 1979 年左右，是早期 `file` 命令（用于不依赖扩展名识别文件类型）源代码的一部分。代码中定义了一个名为 `english(bp, n)` 的函数，用于根据统计特征判断长度为 `n` 的文本 `bp` 是否为英文内容。

```c
// https://www.tuhs.org/cgi-bin/utree.pl?file=V7/usr/src/cmd/file.c
```

![](img1.png)

这个函数使用了一些简单的统计启发规则，基于以下几个语言统计特征来判断文本是否为英语：

* 元音字母的比例
* 高频英文字母（e、t、a、i、o、n）出现的频率
* 罕见英文字母（v、j、k、q、x、z）的比例
* 标点符号的合理性，即标点后面是否缺少空格或换行符
* 特殊（非自然语言）符号的比例，例如 <、> 等 shell 脚本中常用的符号

一段“像”英语的文本应该足够长、标点用得正常、元音字母够多、英文中最常用的字母占优势，而且不能像代码那样满是奇怪的符号。

```c
english (bp, n)
char *bp;
{
# define NASC 128
	int ct[NASC], j, vow, freq, rare;
	int badpun = 0, punct = 0;
	if (n<50) return(0); /* no point in statistics on squibs */
	for(j=0; j<NASC; j++)
		ct[j]=0;
	for(j=0; j<n; j++)
	{
		if (bp[j]<NASC)
			ct[bp[j]|040]++;
		switch (bp[j])
		{
		case '.': 
		case ',': 
		case ')': 
		case '%':
		case ';': 
		case ':': 
		case '?':
			punct++;
			if ( j < n-1 &&
			    bp[j+1] != ' ' &&
			    bp[j+1] != '\n')
				badpun++;
		}
	}
	if (badpun*5 > punct)
		return(0);
	vow = ct['a'] + ct['e'] + ct['i'] + ct['o'] + ct['u'];
	freq = ct['e'] + ct['t'] + ct['a'] + ct['i'] + ct['o'] + ct['n'];
	rare = ct['v'] + ct['j'] + ct['k'] + ct['q'] + ct['x'] + ct['z'];
	if (2*ct[';'] > ct['e']) return(0);
	if ( (ct['>']+ct['<']+ct['/'])>ct['e']) return(0); /* shell file test */
	return (vow*5 >= n-ct[' '] && freq >= 10*rare);
}
```