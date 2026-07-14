# 租事無憂 Jekyll 網站

## 上架到 Render 完整步驟

### Step 1：上傳到 GitHub

1. 前往 github.com → 右上角 `+` → `New repository`
2. 名稱：`rentfreely-site`，選 `Public`，不要勾選任何初始化選項
3. 點 `Create repository`
4. 進入 repository → `Add file` → `Upload files`
5. **把 jekyll-site 資料夾裡的所有檔案和資料夾拖進去**
6. 按 `Commit changes`

### Step 2：部署到 Render

1. 前往 render.com，用 GitHub 帳號登入
2. 點 `New +` → `Static Site`
3. 選擇你的 `rentfreely-site` repository
4. 填入設定：
   - **Name**：rentfreely（或任何名稱）
   - **Build Command**：`bundle install && bundle exec jekyll build`
   - **Publish Directory**：`_site`
5. 點 `Create Static Site`，等約 3～5 分鐘

Render 會給你網址：`https://rentfreely.onrender.com`

### Step 3：更新網站網址（重要！）

部署完成後，到 GitHub 修改 `_config.yml` 第 5 行：
```yaml
url: "https://你的實際render網址.onrender.com"
```
修改存檔後 Render 會自動重新部署。

---

## 申請 Google AdSense

1. 前往 https://www.google.com/adsense/
2. 填入你的 Render 網址
3. 審核約 2～4 週
4. 核准後在 `_includes/head.html` 加入 AdSense 代碼

## 申請 Google Search Console

1. 前往 https://search.google.com/search-console
2. 新增網域，填入 Render 網址
3. 提交 sitemap：`你的網址/sitemap.xml`

## 新增文章

在 `_articles/` 資料夾新增 `.md` 檔：

```
---
layout: article
title: "文章標題"
slug: url-slug
date: 2026-02-01
category: landlord   ← landlord / tenant / rules
category_name: 房東專區
description: "文章簡介"
tags: ["租屋", "hot"]
---

文章內容（HTML 格式）
```

新增後 push 到 GitHub，Render 自動重新部署。

## 未來買網域後

1. 到 `_config.yml` 把 url 改成正式網址
2. 在網域商設定 CNAME 指向 Render
3. Render Dashboard → Custom Domain 綁定網址

## 📄 文章獨立網址（SEO / 社群分享）重要說明

全站 60 篇文章位於 `_articles/`，每篇皆有獨立網址：`https://你的網域/articles/<slug>/`，
由 Jekyll collection 自動產生頁面、加入 sitemap.xml（jekyll-sitemap）並帶有 OG 分享標籤（jekyll-seo-tag）。

**後續新增文章請務必：**
1. 將 `.md` 檔放入 `_articles/`（不要放 `_posts/`，`_posts` 不會被網站讀取）。
2. 檔案開頭必須包含 front matter：

```yaml
---
title: "文章標題"
description: "80~110 字摘要（會成為搜尋結果與社群分享的描述）"
category: landlord   # landlord / tenant / rules 三選一
slug: english-url-keywords   # 決定獨立網址 /articles/<slug>/，請用英文小寫與連字號
date: 2026-07-13
tags: [new]          # 可選：hot / new / fav
---
```

3. 推送部署後，該文章即自動出現在 `/articles/` 列表、擁有獨立可分享網址並被搜尋引擎收錄。
   `generate_content.py` 已更新為自動輸出至 `_articles/` 並自動補 front matter。

## 🌐 正式網域（已完成綁定：rentfreelylife.com）

全站正式網址為 https://rentfreelylife.com（Render 已綁定自訂網域；rentfreely-site.onrender.com 仍可存取並由 Render 自動導向）。
`_config.yml`、`robots.txt`、`llms.txt` 已全部指向正式網域。

後續待辦：
1. GSC 以「網域」資源驗證 rentfreelylife.com，提交 https://rentfreelylife.com/sitemap.xml。
2. AdSense → Sites 移除 onrender 站點，新增 rentfreelylife.com 後要求審核（ads.txt 已就位）。
3. 社群簡介與 LINE 圖文選單的網站連結統一改為 https://rentfreelylife.com。

⚠️ 提醒：IG／Threads 帳號名稱 @rentfreely.life 為社群帳號識別，與網站網域不同屬正常，無需變更。
