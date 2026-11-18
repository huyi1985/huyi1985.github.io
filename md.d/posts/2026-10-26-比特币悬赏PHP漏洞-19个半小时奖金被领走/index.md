---
title: 比特币悬赏PHP漏洞：19个半小时奖金被领走
date: '2026-10-26'
tags:
- shell
- PHP
- 代码
- 内存
- HTTP
- HTTPS
- Web
- 网站
---

# 比特币悬赏PHP漏洞：19个半小时奖金被领走

2026 年 10 月 20 日，PHP 高危漏洞“php2shell”曝光。但这个漏洞究竟能不能被真正利用，一度受到质疑。一方面，ASLR（地址空间布局随机化）会打乱程序的内存布局，攻击者很难提前判断应该跳转到哪里；另一方面，当时几乎没有能够完整实现远程代码执行（RCE）的公开利用代码。

于是，有人决定拿真金白银来验证。10 月 24 日，他搭建了一个名为 stealmybitcoin.com 的网站，故意不修补漏洞，还挂出了一个价值约 503 美元的比特币钱包，向黑客发起挑战。大约 14 个小时后，悬赏金额涨到了约 2014 美元。

挑战开始仅 19 个半小时后，就有人编写出了可用的漏洞利用代码，网站随即被攻破，“奖金”也被领走了。

网站被攻破前，web.archive.org 的存档曾两次因 502 错误而无法访问。

----

https://web.archive.org/web/20260000000000*/stealmybitcoin.com

https://web.archive.org/web/20261024214037/https://stealmybitcoin.com/
https://web.archive.org/web/20261024225724/https://stealmybitcoin.com/

https://web.archive.org/web/20261025000459/https://stealmybitcoin.com/
https://web.archive.org/web/20261025110137/https://stealmybitcoin.com/
https://web.archive.org/web/20261025131700/https://stealmybitcoin.com/
https://web.archive.org/web/20261025164343/https://stealmybitcoin.com/

https://web.archive.org/web/20261025173500/https://stealmybitcoin.com/
https://web.archive.org/web/20261025173500/https://stealmybitcoin.com/

https://web.archive.org/web/20261026001211/http://stealmybitcoin.com/
https://web.archive.org/web/20261026030013/http://stealmybitcoin.com/