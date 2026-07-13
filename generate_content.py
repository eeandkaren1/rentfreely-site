import os
import requests
import pandas as pd
from datetime import datetime

# ================= 1. 基礎設定 =================
EXCEL_PATH = r"C:\Users\USER\Desktop\創業資料\租事無憂_上架完整包_已修正\jekyll-site\_data\365天內容行銷資料庫.xlsx"
SHEET_NAME = "365天日曆"
ARTICLES_DIR = r"C:\Users\USER\Desktop\創業資料\租事無憂_上架完整包_已修正\jekyll-site\_posts"
DIFY_API_URL = "http://localhost/v1/workflows/run" 
DIFY_API_KEY = "app-VLaWmwuWyRmEn6WiPJKZQlO5"

# 建立資料夾
os.makedirs(ARTICLES_DIR, exist_ok=True)

def generate_daily_content(target_day):
    print(f"🚌 開始為 Day {target_day} 撈取資料...")
    
    # 檢查 Excel 是否存在
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ 找不到 Excel 檔案，請確認路徑：{EXCEL_PATH}")
        return
    
    # 讀取 Excel
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, engine="openpyxl")
    except Exception as e:
        print(f"❌ 讀取 Excel 失敗：{e}")
        return

    # 處理 Excel 資料
    df.columns = df.columns.str.strip()
    df['Day'] = df['Day'].astype(str).str.strip()
    row_data = df[df['Day'] == str(target_day)]
    
    if row_data.empty:
        print(f"❌ 在 Excel 中找不到 Day {target_day} 的資料。")
        return
    
    item = row_data.iloc[0]
    seo_topic = str(item.get('SEO文章上稿', '－')).strip()
    threads_topic = str(item.get('Threads貼文主題', '－')).strip()
    fb_topic = str(item.get('Facebook粉專貼文主題', '－')).strip()
    
    print(f"🤖 正在呼叫 Dify API 生成內容 (Topic: {seo_topic})...")
    
    # 呼叫 Dify
    headers = {"Authorization": f"Bearer {DIFY_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "inputs": {"day": str(target_day), "seo_topic": seo_topic, "threads_topic": threads_topic, "fb_topic": fb_topic},
        "response_mode": "blocking",
        "user": "bella-brand"
    }
    
    try:
        response = requests.post(DIFY_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        res_data = response.json()
        
        # 【修正重點】：明確指定抓取 final_content
        outputs = res_data.get('data', {}).get('outputs', {})
        ai_output = outputs.get('final_content', '')
        
        if not ai_output:
            print("❌ 警告：未從 Dify 抓到 final_content 內容，請檢查 Dify 輸出設定。")
            return
            
    except Exception as e:
        print(f"❌ 呼叫 Dify 失敗：{e}")
        return

    # 寫入檔案
    today_str = datetime.today().strftime('%Y-%m-%d')
    log_filename = os.path.join(ARTICLES_DIR, f"{today_str}-day{target_day}.md")
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write(str(ai_output))
    
    print(f"💾 檔案已成功生成：{log_filename}")

if __name__ == "__main__":
    generate_daily_content(1)