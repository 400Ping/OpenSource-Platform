import os
import requests
import csv
import json

def fetch_guardian_news(api_key):
    """
    使用 The Guardian API 的 "search" endpoint 取得新聞資料。
    可自行調整查詢參數。
    """
    url = "https://content.guardianapis.com/search"
    params = {
        "api-key": api_key,
        "section": "world",     # 例如抓取世界新聞分類，可修改成其他分類
        "page-size": 5          # 限制一次抓取的篇數，根據需求調整（免費版可能有篇數限制）
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - 無法取得資料")
        return None

def save_to_csv(results, filename="api.csv"):
    """
    將 API 回傳結果中 "response" -> "results" 部分所包含的每篇新聞資料，
    挑選出重點欄位存成 CSV 檔案。
    """
    fieldnames = [
        "id", 
        "type", 
        "sectionId", 
        "sectionName", 
        "webPublicationDate", 
        "webTitle", 
        "webUrl"
    ]
    
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in results:
            writer.writerow({
                "id": item.get("id"),
                "type": item.get("type"),
                "sectionId": item.get("sectionId"),
                "sectionName": item.get("sectionName"),
                "webPublicationDate": item.get("webPublicationDate"),
                "webTitle": item.get("webTitle"),
                "webUrl": item.get("webUrl")
            })

if __name__ == "__main__":
    # 從環境變數讀取 API 金鑰，若未設定則提醒使用者
    API_KEY = os.getenv("GUARDIAN_API_KEY")
    if not API_KEY:
        raise ValueError("請設定環境變數 GUARDIAN_API_KEY")
    
    data = fetch_guardian_news(API_KEY)
    if data:
        # 取得 "response" 底下的 "results" 部分資料
        results = data.get("response", {}).get("results", [])
        
        # 儲存重點欄位為 CSV 檔案
        save_to_csv(results, "api.csv")
        
        print("API爬蟲執行完畢，已輸出 api.json 與 api.csv")
    else:
        print("API資料取得失敗。")
