import os
from datetime import datetime

from src.crawl import crawl_news
from dotenv import load_dotenv

load_dotenv()

def main():
    openapi_key = os.environ.get("OPENAI_API_KEY")

    urls = {
        "economics": "https://www.msn.com/ko-kr/channel/topic/%EA%B2%BD%EC%A0%9C%ED%95%99/tp-Y_55a61254-2d9d-4a2a-813f-8197f063dda3?ocid=msedgntp",
        "politics_kr": "https://www.msn.com/ko-kr/channel/topic/%EC%A0%95%EC%B9%98/tp-Y_6aa79722-759d-4dbc-af04-abaabe57a18f?ocid=msedgntp",
        "politics_world": "https://www.msn.com/ko-kr/channel/topic/%EC%A0%95%EC%B9%98%20%EA%B3%BC%ED%95%99/tp-Y_e756b287-f1d3-471f-82e3-cec8cf485a26?ocid=msedgntp",
        "entertainment": "https://www.msn.com/ko-kr/channel/topic/%EC%97%B0%EC%98%88%EC%9D%B8/tp-Y_94abd02a-491e-4628-abc7-389d81057107?ocid=msedgntp",
        "sports": "https://www.msn.com/ko-kr/channel/topic/%EC%8A%A4%ED%8F%AC%EC%B8%A0/tp-Y_bc40ffcd-5e18-475c-8752-cb7ca85085a9?ocid=msedgntp",
        "football": "https://www.msn.com/ko-kr/channel/topic/%EC%B6%95%EA%B5%AC/tp-Y_1b38bbd7-c382-4735-a899-86bf31bb9aaa?ocid=msedgntp",
        "baseball": "https://www.msn.com/ko-kr/channel/topic/%EC%95%BC%EA%B5%AC/tp-Y_5accb953-6c7e-4057-bc09-610992e2bfb6?ocid=msedgntp",
        "science": "https://www.msn.com/ko-kr/channel/topic/%EA%B3%BC%ED%95%99/tp-Y_29b23e83-a259-45a8-8479-c0639973ddf4?ocid=msedgntp",
        "crypto": "https://www.msn.com/ko-kr/channel/topic/Cryptocurrency/tp-Y_87a77dbc-3ef7-47f7-ac5a-049eb0d45dd7?ocid=msedgntp",
        "health": "https://www.msn.com/ko-kr/channel/topic/%EC%9D%98%ED%95%99%20%EB%B0%8F%20%EA%B1%B4%EA%B0%95%20%EA%B4%80%EB%A6%AC/tp-Y_6719060b-8fe5-458c-8ad0-ce8a6fae4e87?ocid=msedgntp",
        "automobile": "https://www.msn.com/ko-kr/channel/topic/%EC%9E%90%EB%8F%99%EC%B0%A8%20%EC%82%B0%EC%97%85/tp-Y_6a683b43-36dd-4760-988e-af1164d8823a?ocid=msedgntp",
        "currency": "https://www.msn.com/ko-kr/channel/topic/%ED%86%B5%ED%99%94/tp-Y_386fbf94-4812-4558-8896-67d681dec2b7?ocid=msedgntp",
        "stock": "https://www.msn.com/ko-kr/channel/topic/%EC%A3%BC%EC%8B%9D/tp-Y_6248fde0-7ffd-41ea-98c3-97f089e2a8b0?ocid=msedgntp",
        "MLB": "https://www.msn.com/ko-kr/channel/topic/MLB/tp-Y_bf6ee623-6155-4266-b513-5b854de7a8ef?ocid=msedgntp",
        "history": "https://www.msn.com/ko-kr/channel/topic/%EC%97%AD%EC%82%AC/tp-Y_7af2f24c-fb58-4e34-8e33-ef9b0e1c99de?ocid=msedgntp"        
    }
    today = datetime.now().strftime('%Y%m%d')
    crawl_news(today, urls, openapi_key, max_links=5)
    
if __name__ == "__main__":
    main()