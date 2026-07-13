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
