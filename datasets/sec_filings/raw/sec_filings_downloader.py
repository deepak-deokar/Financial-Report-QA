# datasets/scripts/sec_filings_downloader.py

from sec_edgar_downloader import Downloader

# Your email + company (required)
YOUR_EMAIL = "deepakdeokar1250@gmail.com"
YOUR_COMPANY = "Finance-Enterprise-Document-Q-A"

# Initialize downloader (v5.0.3 → no dir argument)
dl = Downloader(company_name=YOUR_COMPANY, email_address=YOUR_EMAIL)

# Companies
COMPANIES = ["AAPL", "MSFT", "GOOG", "META", "AMZN"]

# Document types
DOC_TYPES = ["10-K", "10-Q"]

# Number of filings
NUM_DOCS = 20

# Download loop
for ticker in COMPANIES:
    for doc_type in DOC_TYPES:
        print(f"Downloading {doc_type} for {ticker}...")
        dl.get(doc_type, ticker, limit=NUM_DOCS)

print("✅ SEC filings download complete! Saved to: ~/.sec-edgar-filings")