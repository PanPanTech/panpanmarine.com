# panpanmarine.com — 站点说明（给 Claude / 任何 AI 助手）

## 站点定位
- PanPan Marine（PanPanTech 旗下品牌）英文 B2B 站，面向海外工业采购：**水下检测 ROV、隧洞检测、水下清洗/清淤机器人、水面清洁/测量无人船、海洋观测设备**。
- 设备由制造商 Boya Gongdao / ROBOOCEAN 生产；PanPan Marine 是销售与项目对接方，**不是制造商，不是独家代理**。
- 目标：Google 自然搜索 + AI 搜索（ChatGPT / Perplexity / Google AI 模式）引用 → 项目询盘（/request-a-proposal/）。
- 市场：全球英文。

## 品牌事实（所有页面、JSON-LD、llms.txt 必须一致；来源 `config.json`）
- 品牌：PanPan Marine；运营主体：Guangzhou PanPanTech Co., Ltd.
- 询盘邮箱：panda@panpantechnology.com；电话：未公开（`contact_phone` 为空）— TODO：是否公开电话/WhatsApp（分支 `cursor/update-public-contact-3d3b` 有未合并的联系方式改动，需人工确认）
- `authorization_verified: false`：在授权文件核实前，不得写“authorized distributor / exclusive”。
- **不宣称**：独家代理、未核实的 CE 认证、海外维修中心、保证交期/保证性能。制造商案例不能写成 PanPan Marine 自己交付的项目。
- 无人船标注“出口需审批（export subject to approval）”。
- 已知资料差异要保留说明：R-30/R-45 图片与参数可能对应不同版本；AD-400 官网 5 km vs 手册 5.5 km；AD-100 的 5 m³/h 指配套分离系统，不是机器人清淤效率。
- 产品线（19 个型号）：R-20 / R-30 / R-45 检测 ROV，AD-400 隧洞检测 ROV，R-150 / R-400 / R-2000 / R-4000 作业级 ROV，A-30 / A-400 爬行检测机器人，A-80 清洗机器人，AD-100 清淤机器人，USUG Skaters 测量船、S-Cleaner / M-Cleaner 水面清洁船、USOL10 观测船、USTL15 运输船，HY-FB-GX01 光学浮标、GL-1300 水下滑翔机，外加 ROV 工具配件页。
- 不确定的事实（价格、认证、交期、案例）不要编造，留 TODO 让人工确认。

## 外链红线（validate.py 会校验，违反即构建失败）
- **禁止**链接或提及制造商网站/联系方式（boyagongdao、roboocean.com、robosea 等）。引用厂家资料只写文字来源，`url` 留空；需要链接时指向站内产品页/案例页。

## 关键词策略
- TODO：GSC/GA4 数据尚未拉取（2026-11-24 体检时浏览器未登录 Google），以下为按站点结构推定的方向，拿到 GSC 后修订。
- **主攻（商业意图）**：inspection ROV / industrial inspection ROV、tunnel inspection ROV、flooded tunnel inspection、underwater trash rack cleaning robot、sump / underwater dredging robot、water surface cleaning vessel / trash skimmer boat、unmanned survey vessel (bathymetry)、light work class ROV。
- **AI 引用型问句**（适合博客开头直接回答）：ROV depth rating、ROV tether length、payload capacity、battery vs tethered mini ROV、observation vs work class ROV、inspection ROV cost / TCO、importing ROV compliance。
- **不追**：消费级/娱乐水下无人机（underwater drone for fishing、Chasing / QYSEA 消费机型参数）、DIY ROV、ROV pilot jobs/培训招聘、海洋科研学术词——不转化。
- **不追**：品牌导航词指向制造商（boya gongdao / roboocean 官网、联系方式）——外链红线，不做。

## 内容规范
- 博客源文件在 `content/blog/<slug>.json`（复制 `_template.json`），字段：answer（开头直接回答）、sections、faq、sources、related_paths。详见 `BLOG_PUBLISHING.md`。
- 每篇：开头 40–60 字直接回答 → 适用条件 / 对比表 → 采购所需数据 → FAQ（页面可见且与 FAQPage JSON-LD 一致）→ 项目询盘入口。
- 所有性能数字注明来源、版本和条件；不虚构工程师署名、客户评价、认证。
- 标题 ≤ 60 字符，description ≤ 155 字符。
- 内链：博客 → 应用页（/solutions/…）/ 产品页（/equipment/…）→ /request-a-proposal/。正文只能链接发布日期不晚于本文的文章。
- 当前定时文章已全部发布完（最后一篇 2026-11-13）；之后没有排期 — TODO：补后续选题。

## 技术 / 部署
- 纯静态站，Python 3 标准库生成：`build.py`（全站）+ `marine_blog.py`（博客、RSS、主题页）；输出 `dist/`。
- 托管：GitHub Pages，`.github/workflows/pages.yml` 在 push `main`、手动触发、以及**每天 00:05 UTC 定时**从 GitHub 上的 `main` 构建（不是本地工作区），所以只要合并到 main 就会上线。
- CI 跑 `python build.py` → `python validate.py`（需本地 http.server 4173）→ `node --check dist/assets/site.js`，再写入 `dist/CNAME`（www.panpanmarine.com）。
- `.openai/hosting.json` 是旧 Sites 托管的遗留配置；`BLOG_PUBLISHING.md` 第 5 步“通过 Sites 工作流推送”已过时，以 GitHub Pages 为准。TODO：确认 Sites 版本已下线后删除。
- 本地预览：`python build.py` → `python -m http.server 4173 --directory dist --bind 127.0.0.1` → `python validate.py`。预览未来文章用 `BLOG_BUILD_DATE=YYYY-MM-DD python build.py`，**提交前删掉 dist/blog 下的未来文章目录**，否则提前公开。
- 仓库里提交的 `dist/` 可能落后于线上（CI 每次重新构建）；以线上和 CI 产物为准。
- GA4：G-7QZTRGDKB3（账号 PanPanTech 414295528，媒体资源 TODO 确认是否为 561863528），代码在 `dist/assets/site.js` 顶部（`build.py` 引用 `site.js?v=…`，改 site.js 后记得更新版本号）。
- 询盘表单（/request-a-proposal/）→ `https://inquiry.panpantechnology.com/api/inquiries`，`lead_brand: "PanPan Marine"`，进飞书 + Zoho；失败时可下载 brief 或打开邮件草稿。
- 转化事件：TODO — 目前**未发送 `generate_lead`**；应在提交成功和邮件兜底时发 `generate_lead`，mailto 点击发 `contact_click`，并在 GA4 设为关键事件。
- llms.txt：TODO — 目前没有（线上 404），应由 build.py 生成并纳入校验。
- 危险操作：不要 force push `main`；不要手改 `dist/` 下由 build.py 生成的 HTML（会被下次构建覆盖），改源码再构建；不要提交凭据。

## 工作流
- 新改动开分支 `seo/<主题>-<MMDD>` 或 `post/<slug>-<MMDD>`，`python validate.py` 通过后合并 main。
- 每周看 GSC：曝光高 + 点击率 < 1% 的页面优先改标题和开头；问句型查询排名靠前但 0 点击的，补直接结论和询盘入口。
- 跨站规范见 `E:\桌面\SEO`（总控）。
