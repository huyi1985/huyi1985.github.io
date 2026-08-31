---
title: PHP有了新搭档：缝合怪FrankenPHP！
date: '2025-06-24'
---

# PHP有了新搭档：缝合怪FrankenPHP！

FrankenPHP 由 Symfony 项目核心开发者之一 Kévin Dunglas 打造，是一个基于 Go 开发的高性能应用服务器，通过与下一代 Web 服务器 Caddy 的紧密集成，在提升运行效率的同时，也简化了部署、运维流程。

![](img1.webp)

FrankenPHP 是将 PHP 解释器（准确来说是 embed SAPI）作为模块直接集成进了 Caddy。除此之外，开发者甚至可以使用 Go 语言来编写扩展供 PHP 调用，也可以反过来在 Go 中直接调用 PHP，灵活性非常高。

这个项目为什么叫“FrankenPHP”呢？“Franken”这个词源自玛丽·雪莱的科幻小说《弗兰肯斯坦》（_Frankenstein_）。故事中的弗兰肯斯坦博士将不同尸体的器官拼装起来，赋予其生命，造出了个“怪物”。FrankenPHP 的构成方式与之如出一辙——PHP、Go 和 Caddy 各取所长，组合成一个全新形态的运行时。正因如此，它的 Logo 是一头脑门上缝着手术线的僵尸大象。

![](img2.png)

FrankenPHP 最具代表性的功能之一无疑是 worker 模式了。

![](img3.png)

传统 PHP 应用的模式是“请求来一个，就初始化一次”。每当有 HTTP 请求到来，PHP 应用都不得不从零开始，加载——执行——释放，重复做很多原本可以复用的工作。而在 FrankenPHP 的 worker 模式下，PHP 应用可以常驻内存，请求之间共享状态，避免重复启动，从而大幅节省资源、提升性能。

对于像 Symfony、Laravel 这样结构复杂、依赖众多的现代框架，这种优化效果尤其明显。更重要的是，开发者并不需要为了切换到 worker 模式去大动干戈。像 Laravel、Symfony、Yii 等主流框架已原生支持 worker 模式，几乎不需要改动代码，就能直接启用，轻松提升性能。

根据专注于中大型企业电商解决方案的 Sylius 公司的测试数据，在启用 worker 模式后，系统响应时间下降了 80%，而维持相同服务能力所需的服务器数量也减少了近六成。