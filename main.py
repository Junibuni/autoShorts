import os
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

from src.crawler import crawl_news
from src.generate_scripts import articles_to_script

load_dotenv()

def main():
    type = "nate"
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    today = datetime.now().strftime('%Y%m%d')
    save_path = "articles"
    
    kwargs_dict = {
        "today": today,
        "openai_client": openai_client,
        "max_links": 5,
        "save_path": save_path
    }
    
    crawl_news(type, kwargs_dict)
    
    articles_to_script(openai_client, os.path.join(save_path, type, today))
    
if __name__ == "__main__":
    main()