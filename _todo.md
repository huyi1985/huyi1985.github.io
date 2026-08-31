压缩 layouts/my_qr.png，现在4.5MB，太大了
footer增加公众号二维码，就是layouts/my_qr.png
---
freeze 功能
---
GoatCount
---
Buy me coffee、爱发电
----
最简单的办法：给网站加统计

如果这个网站是你自己的，我推荐直接上 Cloudflare Web Analytics。

它不要求网站必须托管在 Cloudflare，GitHub Pages 也可以用。Cloudflare官方目前提供的方式是：

注册/登录 Cloudflare
进入 Web Analytics
Add a site
填：
huyi1985.github.io
Cloudflare给你一段 JS
把 JS 放进网站 HTML 的</body>之前
等数据开始积累

之后就在 Cloudflare 的 Web Analytics 页面看访问数据。Cloudflare明确支持不经过Cloudflare代理的网站，只需要加入一个 JS beacon。

它可以看到包括：

Page views
访问量
页面
国家/地区
Referrer
页面性能
访问趋势

而且是免费的。