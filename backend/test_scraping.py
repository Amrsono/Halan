import requests
import logging

logging.basicConfig(level=logging.INFO)

URLS = {
    "Zeed Gold": "https://zeed.tech/funds/az-gold",
    "Zeed Opps": "https://zeed.tech/funds/az-opportunities",
    "Mubasher Gold": "https://www.mubasher.info/markets/EGX/funds/AZG",
    "Mubasher Opps": "https://www.mubasher.info/markets/EGX/funds/AZO",
    "Thndr Gold": "https://thndr.app/product/AZG"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

with open("scrape_results.txt", "w", encoding="utf-8") as f:
    for name, url in URLS.items():
        try:
            f.write(f"Testing {name}: {url}\n")
            resp = requests.get(url, headers=HEADERS, timeout=10)
            f.write(f"Status: {resp.status_code}\n")
            if resp.status_code == 200:
                f.write(f"Content Length: {len(resp.text)}\n")
                if "Cloudflare" in resp.text:
                    f.write("Result: Cloudflare detected\n")
                else:
                    f.write("Result: Success\n")
            else:
                f.write("Result: Failed\n")
        except Exception as e:
            f.write(f"Result: Error {e}\n")
        f.write("-" * 30 + "\n")
