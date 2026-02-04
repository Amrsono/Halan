import yfinance as yf

TICKERS = [
    "AZG.CA", "AZO.CA", "EGX30.CA", "^CASE30", "EGP=X", "AXA.CA", "COMI.CA"
]

with open("yfinance_results.txt", "w", encoding="utf-8") as f:
    f.write("Testing Yahoo Finance Tickers:\n")
    f.write("-" * 30 + "\n")
    
    for ticker in TICKERS:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            
            if not hist.empty:
                last_price = hist['Close'].iloc[-1]
                f.write(f"✅ {ticker}: Found! Price: {last_price}\n")
            else:
                f.write(f"❌ {ticker}: No data found\n")
                
        except Exception as e:
            f.write(f"❌ {ticker}: Error - {e}\n")

    f.write("-" * 30 + "\n")
