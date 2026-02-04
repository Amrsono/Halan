import requests
import logging

logging.basicConfig(level=logging.INFO)

URL = "https://egx.com.eg/en/MutualFunds.aspx"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    print(f"Fetching {URL}...")
    resp = requests.get(URL, headers=HEADERS, timeout=15, verify=False)
    print(f"Status: {resp.status_code}")
    
    with open("egx_page.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
    print("Saved to egx_page.html")
    
except Exception as e:
    print(f"Error: {e}")
