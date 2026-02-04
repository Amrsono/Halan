import requests
import logging

logging.basicConfig(level=logging.INFO)

URLS = {
    # Official EGX Site (Likely best source for raw data)
    "EGX Funds": "https://egx.com.eg/en/MutualFunds.aspx",
    
    # Mubasher specific fund pages
    "Mubasher Gold": "https://www.mubasher.info/markets/EGX/funds/AZG",
    "Mubasher Opps": "https://www.mubasher.info/markets/EGX/funds/AZO",
    
    # Thndr Product Pages
    "Thndr Gold": "https://thndr.app/product/AZG",
    "Thndr Opps": "https://thndr.app/product/AZO"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

with open("scrape_v2_results.txt", "w", encoding="utf-8") as f:
    for name, url in URLS.items():
        try:
            f.write(f"Testing {name}: {url}\n")
            # Increased timeout and verify=False to ignore SSL cert issues if any exist
            resp = requests.get(url, headers=HEADERS, timeout=15, verify=False)
            f.write(f"Status: {resp.status_code}\n")
            if resp.status_code == 200:
                f.write(f"Content Length: {len(resp.text)}\n")
                if "Cloudflare" in resp.text:
                    f.write("Result: Cloudflare detected\n")
                elif "azimut" in resp.text.lower() or "gold" in resp.text.lower():
                     f.write("Result: Success (Keywords found)\n")
                else:
                     f.write("Result: Success (But keywords missing??)\n")
            else:
                f.write("Result: Failed\n")
        except Exception as e:
            f.write(f"Result: Error {e}\n")
        f.write("-" * 30 + "\n")
