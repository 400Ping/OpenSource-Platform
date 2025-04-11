import requests
from bs4 import BeautifulSoup
import csv
import json

def crawl_ptt_gossiping():
    # Gossiping 版網址，需要透過 cookies 送出 over18
    url = "https://www.ptt.cc/bbs/Gossiping/index.html"
    cookies = {"over18": "1"}
    response = requests.get(url, cookies=cookies)
    
    if response.status_code != 200:
        print("請求失敗，狀態碼:", response.status_code)
        return None, None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 取得頁面標題
    page_title = soup.title.string if soup.title else "無標題"
    print("頁面標題:", page_title)
    
    # 擷取所有文章列表，每篇文章區塊都包在 div.r-ent 中
    posts = soup.find_all("div", class_="r-ent")
    post_list = []
    
    for post in posts:
        # 標題區塊通常在 div.title 中
        title_elem = post.find("div", class_="title")
        title = title_elem.get_text(strip=True) if title_elem else ""
        
        # 取得文章連結（部分文章可能因被刪除而無法取得連結）
        link_tag = title_elem.find("a") if title_elem else None
        link = "https://www.ptt.cc" + link_tag["href"] if link_tag and "href" in link_tag.attrs else ""
        
        # 取得作者
        author_elem = post.find("div", class_="author")
        author = author_elem.get_text(strip=True) if author_elem else ""
        
        # 取得日期（版面上日期通常只提供月日）
        date_elem = post.find("div", class_="date")
        date = date_elem.get_text(strip=True) if date_elem else ""
        
        # 取得文章熱門程度（點數/推文數），通常存在 div.nrec 區塊中
        nrec_elem = post.find("div", class_="nrec")
        nrec = nrec_elem.get_text(strip=True) if nrec_elem else ""
        
        post_list.append({
            "標題": title,
            "作者": author,
            "日期": date,
            "連結": link,
            "熱門程度": nrec
        })
    
    return page_title, post_list

def save_to_csv(filename, data, header):
    with open(filename, "w", encoding="utf-8", newline="") as csvfile:
         writer = csv.DictWriter(csvfile, fieldnames=header)
         writer.writeheader()
         for row in data:
             writer.writerow(row)

def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as jsonfile:
         json.dump(data, jsonfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    page_title, posts = crawl_ptt_gossiping()
    
    if posts is not None:
        csv_filename = "static.csv"
        json_filename = "static.json"
        header = ["標題", "作者", "日期", "連結", "熱門程度"]
        save_to_csv(csv_filename, posts, header)
        save_to_json(json_filename, posts)
        print("已成功爬取 PTT Gossiping 版的文章資訊並分別儲存至", csv_filename, "及", json_filename)
    else:
        print("爬取失敗。")
