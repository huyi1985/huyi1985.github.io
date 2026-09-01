
# 盈利路线（详见 claudedocs/monetization-roadmap.md）
顺序：域名 → 索引 → 流量 → 变现（跳步=空转）

## P0 现在
- [ ] 买独立域名 → CNAME 指向 GitHub Pages → Enforce HTTPS → 改 config.toml baseURL → 放 CNAME 文件 → 重提 sitemap（github.io 子域 AdSense 不过审）
- [ ] Google Search Console 验证（DNS TXT 或已埋的 google-site-verification meta）→ 提交 sitemap.xml → 请求关键页索引
- [ ] GoatCounter 后台开 "Allow adding visitor counts on your website"（代码已就绪，开了才有阅读量数字）

## P1 流量前置
- [ ] baseof.html 加 Open Graph + Twitter Card meta（分享卡预览，传播/带货前置）
- [ ] 补 About / 联系 / 隐私政策 页（AdSense 与联盟申请常要）
- [ ] Buy me coffee / 爱发电 按钮挂 footer 或文末（最快变现上线，零门槛）
- [ ] Cloudflare 兜底：域名 NS 托管 → 开代理 → 缓存/压缩规则（国内访问兜底）

## P2 变现接入（流量起来后）
- [ ] AdSense 申请（域名+合规页就绪后）→ 过审填 ad-slot partial
- [ ] 带货选品：豆瓣阅读/极客时间/Amazon → 商品卡 partial → 编辑相关文章挂链
- [ ] 内容从计算机历史向宽科技/编程扩展（保持"历史+实用"双锚，防发散）

## P3 进阶
- [ ] Article schema.org JSON-LD（富摘要 SEO）
- [ ] 国内备案（等 GoatCounter 地域数据证明国内占比高再投）

----
历史：
- ✅ 统计：GoatCounter（免费层、商用许可）已接，每篇阅读量端点已实现
- ✅ SEO：sitemap/robots/keywords meta/canonical/tag 聚合页（184 个）
- ✅ 广告位 partial ad-slot.html 已留位（enabled=false）
- ✅ 228 篇文章上线，221 篇自动打 tag（3180 个）
