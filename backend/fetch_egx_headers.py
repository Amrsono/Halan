import requests
import logging

logging.basicConfig(level=logging.INFO)

URL = "https://www.egx.com.eg/en/MutualFunds.aspx"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.egx.com.eg/en/Homepage.aspx",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1"
}

try:
    print(f"Fetching {URL} with full headers...")
    resp = requests.get(URL, headers=HEADERS, timeout=15, verify=False)
    print(f"Status: {resp.status_code}")
    print(f"Length: {len(resp.text)}")
    
    with open("egx_page_full.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
        
    if "Azimut" in resp.text:
        print("✅ Found Azimut")
    else:
        print("❌ Azimut not found")
        
except Exception as e:
    print(f"Error: {e}")
