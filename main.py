import os
from datetime import datetime

from src.crawl import crawl_news

def main():
    topics = [
        "economics",
        "entertainment",
        "politics",
        "sports"
    ]
    today = datetime.now().strftime('%Y%m%d')
    crawl_news(today, max_links=20)
    
if __name__ == "__main__":
    main()