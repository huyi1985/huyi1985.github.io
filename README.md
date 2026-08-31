# 《计算机历史·奇闻与资料库》站点

中文计算机历史知识站 MVP：把 `/Users/huyi/Projects/unix-history-docs` 等源目录里的文章，经**流水线**整理后用 Hugo 构建静态站，按时间展示、按标签筛选，广告位模板预留。

## 流水线架构（3 阶段，全部已实现）

```
源目录（~140 篇中文文章，各含 md+图片，md 内图片用图床地址）
   │
   │ ①  collect_posts.py
   ▼
raw_md.d/   ← 纯 md 提取物（扁平，一篇文章一个 md；图片不在此阶段处理）
   │
   │ ②  download_images.py
   │     解析 md 里 ![..](https://图床/..)：图床图下载 → raw_md.d/assets/，
   │     转 WebP（cwebp/sips/Pillow），改写 md 引用为绝对路径 /assets/xxx.webp
   ▼
（图床图已本地化的一组 md + assets/）
   │
   │ ③  build_md_d.py
   │     raw_md.d → md.d/（frontmatter 规整：去 source，留 title/date/tags；
   │     assets 拷贝到 md.d/assets/，Hugo 静态挂载 /assets/）
   ▼
md.d/  →  Hugo 构建（contentDir=md.d）→ public/ → Cloudflare Pages
```

> `raw_md.d/` 是**中间产物**（阶段①②可重跑）；`md.d/` 是 Hugo 直接消费的内容目录（阶段③产物）。
> 旧结构 `md.d/` 已备份为 `md.d.legacy-20260831/`（7 篇文章 + coffee_stain.png，不再被 Hugo 读取）。

## 结构

```
_niuniu_yiyi/
├── config.toml          # Hugo 配置：contentDir=md.d，/assets/ 静态挂载，广告位开关，baseURL 占位
├── raw_md.d/            # 阶段①②产物：纯 md 提取物 + assets/（图床图已本地化）
├── md.d/                # 阶段③产物：Hugo 内容目录（140 篇 md + assets/）
├── md.d.legacy-20260831/  # 旧结构的整目录备份
├── layouts/             # 极简主题（首页/列表/单篇/标签/广告位）
├── public/              # Hugo 构建产物（本地预览/部署用）
└── scripts/
    ├── collect_posts.py   # 阶段①：提取文章 md → raw_md.d/（幂等 + --force）
    ├── download_images.py # 阶段②：图床图本地化 + WebP 压缩 + 改写引用
    └── build_md_d.py      # 阶段③：raw_md.d → md.d（frontmatter 规整 + assets 拷贝）
```

## 用法

```bash
# 阶段①：提取源目录 md 到 raw_md.d/（只读源目录，不写回）
python3.11 scripts/collect_posts.py --dry-run   # 预览
python3.11 scripts/collect_posts.py             # 执行（目标已存在则跳过）
python3.11 scripts/collect_posts.py --force     # 强制覆盖已存在的目标

# 阶段②：图床图片本地化（幂等；--force 重下已存在的图）
python3.11 scripts/download_images.py --dry-run # 预览
python3.11 scripts/download_images.py           # 下载 + 转 WebP + 改写 md 引用

# 阶段③：重建 md.d/（frontmatter 规整 + 拷贝 assets）
python3.11 scripts/build_md_d.py --dry-run      # 预览
python3.11 scripts/build_md_d.py                # 重建

# 构建 & 本地预览
hugo serve -D        # 本地预览（http://localhost:1313）
hugo                 # 构建到 public/
```

## 图片本地化说明（阶段②行为）

- 图床图下载到 `raw_md.d/assets/`，统一转 WebP（`cwebp -q 80`；透明 PNG 保持原格式；无 cwebp 时回退 sips/Pillow）
- md 里引用改写为绝对路径 `/assets/<文件名>.webp`
- 重复 URL 只下载一次；`--force` 强制重下
- **图床上已删除的图（返回 404）**：md 引用**保持原图床 URL 不变**（不生成假的占位文件），站点上该图自然不显示——本次约 67 张图床图已失联，无法本地化
- `config.toml` 用 `[[module.mounts]]` 把 `md.d/assets` 挂载到站点根 `/assets/`

## 发布时间与标签

- 每篇文章的 `date` 默认取源文件 mtime（可手动改 frontmatter 校准）
- `tags` 由脚本按关键词自动建议（阶段③当前未做 tags 自动建议，留待后续）
- 列表页按 `date` 倒序；`/tags/` 提供标签筛选

## 广告位（预留，未启用）

- `config.toml` → `[params.ads].enabled = false`
- 启用后：填入广告联盟代码到 `layouts/partials/ad-slot.html`
- 正文下方已有占位（`single.html`）

## TODO

- [ ] URL slug 决定：当前 Hugo 默认把中文文件名转小写 ASCII slug（`2025-02-04-20241116-一个神奇的网站...` → `2025-02-04-20241116-一个神奇的网站-0.30000000000000004.com`），需确认是否用英文 slug 更稳
- [ ] tags 自动建议（阶段③当前只保留 title/date）
- [ ] 注册域名，替换 `config.toml` 的 `baseURL`
- [ ] 接入 Cloudflare Pages + GitHub 自动部署
- [ ] 提交百度搜索资源平台 / Bing Webmaster / Google Search Console
- [ ] 校准每篇的真实发布日期
