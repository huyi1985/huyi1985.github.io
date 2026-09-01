---
title: 云风说微信不该用 SQLite，然后技术圈炸了 - OSCHINA - 开源 × AI · 开发者生态社区
date: '2026-07-07'
tags:
- 文件
- Go
- 代码
- 存储
- 性能
- 优化
- HTTP
- HTTPS
- URL
- 开源
- 社区
- grep
- 数据库
- SQL
- 数据
- 索引
- AI
- 大模型
- 模型
- Git
- 开发
- 软件
- 程序员
---

# 云风说微信不该用 SQLite，然后技术圈炸了 - OSCHINA - 开源 × AI · 开发者生态社区

一位开发者提问微信聊天记录存储方式引发中文技术圈争论，云风认为**纯文本**追加优于SQLite，但vczh指出工程实现问题，vczh认为SQLite本身没问题，反对声音还包括用户体验和工程可靠性质疑。技术选型争议分为SQLite与纯文本，深层反映两代人对工程问题定义差异。

总结由社区平台通过AI大模型技术生成

6 月 29 日，一位开发者在 X 上随口问了一句「还是搞不懂为啥你们的微信能聊出几百 G」，结果炸出了中文技术圈过去两天最大的一场争论。

引爆点来自[云风](https://www.oschina.net/news/291324)（@cloudwu）的回复。作为前网易《梦幻西游》《大话西游》引擎架构师，他在中文开发者圈子里有相当的分量。他的原话是：

> 「微信的开发人员根本就不懂该怎么**储存数据。这种聊天软件，文本和媒体文件分开存，文本根本就不应该保存在什么数据库(sqlite)里，一个对话一个文本文件追加就可以了**。需要搜索的时候 grep 一下性能完全符合需求。」

这条推文获得了 26.5 万次浏览、79 条回复、311 条引用——数字背后是一场持续两天仍未平息的技术论战。

云风的核心逻辑很清晰：聊天记录是典型的流式追加数据，不需要对老数据做删改。即使有删除或撤回，记录的也是操作行为本身——「我发了一条消息」「我删了一条消息」——全部按时间顺序追加写入即可。他认为纯文本比数据库更「耐操」：不会因为软件 bug、升级、废弃而损坏；即使有天微信消失了，用户依然能拥有自己的聊天记录。

但反对的声音同样响亮。

轮子哥 vczh（@geniusvczh）一针见血：「明明是一个微信连 SQLite 都用不好的问题，大家非要讨论该不该用 sqlite。」言下之意，SQLite 本身没问题，是微信的工程实现拉了胯。

LIN WEI（@skywind3000）从用户体验角度质疑：「真正问题在于就那么点内容，为啥微信用 sqlite 搜索经常搜出 0.5-1.0 秒来？经常切换应用切回微信时，消息更新直接卡住几秒？电量直接掉 2%，而 telegram 不管多少消息都那么顺滑？」

数据库专家 Vonng（@RonVonng）则从工程可靠性角度反驳云风：「以微信的体量，是不是有资源去自研一个 SQLite？肯定是可以的，但我敢肯定 100% 会比 SQLite 差得远。数据库项目的灵魂不在于代码，而在于可靠性历史战绩证明。手搓一个 PG/SQLite 相当于抛弃了全世界用户场景几十年积累下来的信任。」

DCjanus（@janus_of_DC）用一个生动的比喻点出了这场争论的荒诞之处：讨论「微信消息该不该用 txt + grep 替代 SQLite」，就像一本正经地研究「把空格缩进改成 tab 来优化 Git 仓库体积」——方向没错，但先看看仓库里是不是塞了部 12.7GB 的蓝光片。

这比喻比很多人意识到的更精确。开发者 @tapopat 在讨论中翻出了微信的实际存储格式：聊天记录中的每条消息都用 zstd 压缩后再存入 SQLite，而消息 ID 用的是 MD5 哈希。这意味着微信并非拿 SQLite 当简单的行存储用——它在上面叠加了压缩层和哈希索引，每条消息的存储成本远高于纯文本追加。**一个为关系型查询优化的数据库引擎，被当作压缩 blob 的容器，然后用户抱怨它慢——这不是 SQLite 的问题，是架构设计从一开始就跑偏了**。

还有人试图调和。黄赟说年轻时候也喜欢比谁的 SQL 写得好、性能高，但读完《Oracle Internals》《SQL Server Internals》《RDBMS Internals》之后就不争了——「不敢了，这些市场巨无霸才有争的理由」。孟岩（@myanTokenGeek）则对云风说：「你就不该在这一代程序员面前提出重新发明轮子的想法，他们会很惊骇的。」

回头看，争论其实裂成了两层。

表层是技术选型：聊天记录该用 SQLite 还是纯文本？正方说 SQLite 带来了索引、查询便利、事务安全，是全球 IM 应用的事实标准——iMessage、WhatsApp 都用它，微信还在此基础上做了 WCDB（已开源近十年）。反方说聊天场景的读写模式足够简单，SQLite 在微信手里变成了数据腐败的温床，很多安卓用户都遇到过聊天记录损坏或消失的问题。

底层更耐人寻味：为什么是云风？一个做过大型网游引擎的人，说「不用数据库反而更简单」，这种反直觉的判断让年轻一代开发者既困惑又本能地排斥。这或许不是技术之争，而是两代人对「什么算工程问题」的定义不同。

参考来源：

- [https://x.com/cloudwu/status/2071533904977428611](https://www.oschina.net/action/GoToLink?url=https%3A%2F%2Fx.com%2Fcloudwu%2Fstatus%2F2071533904977428611)
- [https://x.com/passluo/status/2071443107242283128](https://www.oschina.net/action/GoToLink?url=https%3A%2F%2Fx.com%2Fpassluo%2Fstatus%2F2071443107242283128)
- [https://x.com/geniusvczh/status/2072120521677017113](https://www.oschina.net/action/GoToLink?url=https%3A%2F%2Fx.com%2Fgeniusvczh%2Fstatus%2F2072120521677017113)
- [https://x.com/skywind3000/status/2072141863163924739](https://www.oschina.net/action/GoToLink?url=https%3A%2F%2Fx.com%2Fskywind3000%2Fstatus%2F2072141863163924739)
- [https://x.com/RonVonng/status/2072141340536955247](https://www.oschina.net/action/GoToLink?url=https%3A%2F%2Fx.com%2FRonVonng%2Fstatus%2F2072141340536955247)
- [https://x.com/janus_of_DC/status/2072149113626619944](https://www.oschina.net/action/GoToLink?url=https%3A%2F%2Fx.com%2Fjanus_of_DC%2Fstatus%2F2072149113626619944)