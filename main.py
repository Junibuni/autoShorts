import os
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

from src.crawler import crawl_news

load_dotenv()
    
def main():
    type = "nate"
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    today = datetime.now().strftime('%Y%m%d')
    
    kwargs_dict = {
        "today": today,
        "openai_client": openai_client,
        "max_links": 5
    }
    
    crawl_news(type, kwargs_dict)
    
if __name__ == "__main__":
    main()