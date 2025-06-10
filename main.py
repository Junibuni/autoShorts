import os
from datetime import datetime

from src.crawl import crawl_news

def main():
    urls = {
        "economics": "https://www.msn.com/ko-kr/channel/topic/%EA%B2%BD%EC%A0%9C%ED%95%99/tp-Y_55a61254-2d9d-4a2a-813f-8197f063dda3?ocid=msedgntp",
        "politics": "https://www.msn.com/ko-kr/channel/topic/%EC%A0%95%EC%B9%98/tp-Y_6aa79722-759d-4dbc-af04-abaabe57a18f?ocid=msedgntp",
        "entertainment": "https://www.msn.com/ko-kr/channel/topic/%EC%97%B0%EC%98%88%EC%9D%B8/tp-Y_94abd02a-491e-4628-abc7-389d81057107?ocid=msedgntp",
        "sports": "https://www.msn.com/ko-kr/channel/topic/%EC%8A%A4%ED%8F%AC%EC%B8%A0/tp-Y_bc40ffcd-5e18-475c-8752-cb7ca85085a9?ocid=msedgntp",
        "science": "https://www.msn.com/ko-kr/channel/topic/%EA%B3%BC%ED%95%99/tp-Y_29b23e83-a259-45a8-8479-c0639973ddf4?ocid=msedgntp",
        "crypto": "https://www.msn.com/ko-kr/channel/topic/Cryptocurrency/tp-Y_87a77dbc-3ef7-47f7-ac5a-049eb0d45dd7?ocid=msedgntp",
        "health": "https://www.msn.com/ko-kr/channel/topic/%EC%9D%98%ED%95%99%20%EB%B0%8F%20%EA%B1%B4%EA%B0%95%20%EA%B4%80%EB%A6%AC/tp-Y_6719060b-8fe5-458c-8ad0-ce8a6fae4e87?ocid=msedgntp",
        "space": "https://www.msn.com/ko-kr/channel/topic/%EC%9A%B0%EC%A3%BC%20%ED%83%90%EC%82%AC/tp-Y_13001aa7-f0c0-415c-a17b-abff484fd9b3?ocid=msedgntp",
        "automobile": "https://www.msn.com/ko-kr/channel/topic/%EC%9E%90%EB%8F%99%EC%B0%A8%20%EC%82%B0%EC%97%85/tp-Y_6a683b43-36dd-4760-988e-af1164d8823a?ocid=msedgntp",
        "movie": "https://www.msn.com/ko-kr/channel/topic/%EC%98%81%ED%99%94/tp-Y_7a4cb378-5d26-43dd-9492-0099b1b67bbf?ocid=msedgntp",
        "stock": "https://www.msn.com/ko-kr/channel/topic/%EC%A3%BC%EC%8B%9D/tp-Y_6248fde0-7ffd-41ea-98c3-97f089e2a8b0?ocid=msedgntp",
    }
    today = datetime.now().strftime('%Y%m%d')
    crawl_news(today, urls, max_links=5)
    
if __name__ == "__main__":
    main()