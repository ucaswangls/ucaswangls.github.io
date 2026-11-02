# 王理顺的个人主页

基于 Jekyll / al-folio，部署地址：https://ucaswangls.github.io/ 。

## 内容维护

- `_pages/about.md`：个人简介、研究方向与近期进展。
- `_bibliography/papers.bib`：10 篇代表性论文；`selected={true}` 的论文在首页展示。简历未提供的 DOI、链接及完整作者名单未补写；`others` 表示其余作者。
- `_data/cv.yml`：个人履历、荣誉、学术服务与专利，是履历页面的数据源。
- `_pages/projects.md`：主持与参与项目。
- `assets/img/lishun-wang.png`：从用户提供的简历提取的原始头像。
- `_config.yml`：站点域名、个人信息与主题配置。

公开页面只保留专业背景、邮箱和 GitHub 联系方式。原始简历中的手机号、出生日期未放入网站，也未发布原始 PDF。

## 本地构建

使用 Ruby 3.3 与 Bundler：

```sh
bundle install
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 bin/check-site.py _site
bundle exec jekyll serve
```

## GitHub Pages 发布

1. 将本目录中的修改提交并推送至原仓库的 `master`（或 `main`）分支。
2. 在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
3. 在 **Actions** 中启用工作流（如尚未启用），运行 **Build and deploy personal homepage**，或推送一次提交。
4. 构建先生成页面并检查站内链接，成功后部署至 GitHub Pages；PR 只构建，不发布。

站点必须使用 `url: https://ucaswangls.github.io` 和 `baseurl: ""`。此用户主页发布在域名根路径，不使用 `/al-folio`。

## 本次修复

- 修正默认域名和子路径，替换默认个人信息、示例论文及履历。
- 排除示例博客、项目和人员页面，关闭模板外部博文抓取及不需要的图片转换。
- 将向 `gh-pages` 分支写入的旧部署方式替换为官方 Pages artifact 部署，显式声明权限。
- 关闭 CSS 重复压缩，避免构建长时间占用 CPU；Sass 继续输出压缩 CSS。
- 修复小屏幕履历目录遮挡内容，保留桌面端目录。
- 保留 al-folio 的响应式布局、暗色模式与论文搜索。

原主题遵循 MIT License，详见 `LICENSE`。
