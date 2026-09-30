import requests
from bs4 import BeautifulSoup, Comment
import re
import json

url = "https://indriver.com"
my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0"

headers = {
    "User-Agent": my_user_agent,
    "Accept": "text/html,application/xhtml+xml,xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

def crawl_indriver():
    try:
        print(f"Đang truy cập: {url}...")
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"[!] Lỗi truy cập: Status Code {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        results = {
            "emails": [],
            "links": [],
            "js_files": [],
            "images": [],
            "comments": []
        }

        # --- A. Trích xuất Links ---
        for a in soup.find_all('a', href=True):
            results["links"].append(a['href'])
        results["links"] = list(set(results["links"])) # Lọc trùng

        # --- B. Trích xuất JS files ---
        for script in soup.find_all('script', src=True):
            results["js_files"].append(script['src'])
        results["js_files"] = list(set(results["js_files"]))

        # --- C. Trích xuất Images ---
        for img in soup.find_all('img', src=True):
            results["images"].append(img['src'])
        results["images"] = list(set(results["images"]))

        # --- D. Trích xuất Emails (Dùng Regex) ---
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        all_text = soup.get_text()
        results["emails"] = list(set(re.findall(email_regex, all_text)))

        # --- E. Trích xuất Comments HTML ---
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        results["comments"] = [c.strip() for c in comments]

        # 4. Xuất kết quả ra định dạng JSON giống trong báo cáo
        output_json = json.dumps(results, indent=4, ensure_ascii=False)
        print("\n[+] KẾT QUẢ CRAWL:")
        print(output_json)

        # Lưu vào file để nộp kèm bài làm
        with open("bai15_results.json", "w", encoding="utf-8") as f:
            f.write(output_json)
        print("\n[✔] Đã lưu kết quả vào file 'bai15_results.json'")

    except Exception as e:
        print(f"[X] Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    crawl_indriver()
