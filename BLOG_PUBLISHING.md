# PanPan Marine 博客发布手册

主入口：https://www.panpanmarine.com/blog/ 。博客服务海外工业采购，围绕设备选型、隧洞检测、清洗与清淤三个主题持续积累内容。产品页负责规格和询价，博客负责解释采购问题，Resources 保留工具性资料和清单。

## 发布方式

1. 在 `content/blog/` 复制 `_template.json`，改名为文章英文 slug；也可以提供 Markdown 初稿，再转换到此格式。
2. 填写标题、描述、直接答案、章节 HTML、FAQ、来源、图片和内链。图片文件放在 `dist/assets/`，`image` 只填写文件名。所有性能数字注明来源、适用版本和条件。
3. 草稿保持 `status: draft`。审核后改为 `published`，填写实际发布日期和更新日期。仅有实质内容更新时修改 `updated_at`。
4. 运行 `python build.py`，启动 `python -m http.server 4173 --directory dist --bind 127.0.0.1`，再运行 `python validate.py`。检查桌面、手机菜单、表格、图片和询价入口。
5. 通过已有 Sites 工作流推送对应源代码，打包并保存版本、部署，然后同步 GitHub。仅推送 GitHub 不会自动更新现有托管网站。
6. 检查线上文章、博客列表、RSS 和 sitemap。文章发布后再在 Search Console 中观察发现、收录和相关查询表现。

生成器会更新全站 Blog 导航、首页最近三篇文章、应用页相关文章、博客列表、主题页、RSS 和 sitemap。每篇文章有独立 URL、canonical、日期、作者、目录、BlogPosting、FAQPage 和面包屑结构化数据。主题页不足三篇时保留浏览入口但设置 noindex。没有可视化后台或自动定时发布功能；这些内容文件是现阶段的编辑入口。

## 外链红线

全站（产品页、博客、案例、来源列表）**禁止链接到制造商网站**（boyagongdao.com、roboocean.com 等），也不写厂家网址或联系方式，避免客户绕过 PanPan Marine 直接联系厂家。引用厂家资料时只写文字来源（例如 "Manufacturer product information: A-80"，`url` 留空），需要链接时指向站内对应的产品页或案例页。`validate.py` 会检查，出现厂家域名即校验失败。

## 首批与后续选题

| 顺序 | 主题 / 核心关键词 | 目的 | 发布前需要的资料 |
|---|---|---|---|
| 已发布 | industrial inspection ROV selection | 设备初筛 | 厂家版本参数、应用边界 |
| 已发布 | flooded tunnel inspection procurement | 项目准备 | 路线、验收与交付字段 |
| 已发布 | underwater cleaning vs dredging | 工艺初筛 | 沉积物、泵管与分离设备条件 |
| 4 | ROV payload capacity | 解释载荷与整机配置 | 各版本载荷定义与附件重量 |
| 5 | R30 vs R45 inspection ROV | 产品比较 | 同一日期的配置表及适用场景 |
| 6 | ROV depth rating and operating conditions | 避免只按深度选型 | 密封、传感器及线缆配置说明 |
| 7 | flooded tunnel inspection report | 帮助定义验收 | 可公开脱敏报告与原始数据样例 |
| 8 | tunnel inspection ROV tether management | 解释系统采购范围 | 厂家布放回收与绞车方案说明 |
| 9 | industrial ROV total cost of ownership | 项目预算 | 真实备件、培训及维护报价范围 |
| 10 | underwater trash rack cleaning | 细分应用 | 栅间距、材质、附着物及现场照片 |
| 11 | dredging pump pipeline selection | 解释系统匹配 | 输送距离、扬程、粒径、固含量与泵曲线 |
| 12 | underwater sediment removal project brief | 提升询盘质量 | 沉积物分析、体积和处理去向 |

建议初期每月完成两篇有真实依据的文章，并根据询盘问题调整次序。关键词是选题方向，未宣称搜索量。现有 camera-vs-sonar 资源页继续更新，不另外复制同题薄文章。不要把厂家案例写成 PanPan Marine 自有交付，也不要把规划建议写成保证性能。

## 质量与效果

先回答问题，再解释适用条件、比较方法、采购所需数据和下一步。每篇至少连接到相关应用、产品或资料页，并设置项目咨询入口。FAQ 必须在页面上可见并与结构化数据一致。来源优先厂家原始资料及官方技术说明，避免虚构工程师署名、认证、客户评价或海外服务网点。

SEO/GEO 以可抓取、可理解、可核对的内容为基础；标记本身不保证排名、富媒体结果或 AI 引用。观察有效询盘、相关搜索展示、点击和被引用情况，避免仅追求文章数量。
