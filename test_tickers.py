import yfinance as yf

tickers = ["EGP=X", "GC=F", "EGX30.CA", "^CASE30", "COMI.CA"]

print("Testing tickers...")
for ticker in tickers:
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1d")
        if not hist.empty:
            print(f"✅ {ticker}: Success (Last: {hist['Close'].iloc[-1]})")
        else:
            print(f"❌ {ticker}: No data")
    except Exception as e:
        print(f"❌ {ticker}: Error {e}")
