import os

class NATENewsScraper:
    def __init__(self, today, article_path="articles"):
        self.article_path = os.path.join(article_path, "msn")
        
        if not os.path.exists(self.article_path):
            os.makedirs(self.article_path)
            
        today_path = os.path.join(self.article_path, today)
        if not os.path.exists(today_path):
            os.makedirs(today_path)
    
    def get_article_links(self, page):
        pass
    
    def scrape_article(self, page, url):
        pass
    
    def save_article(self, content, url, subject):
        pass
    
    def run(self, subject, topic_url):
        pass

def crawl_news(today, max_links=20):
    scraper = NATENewsScraper(
        today
    )
    
    from src.urls import URLS_NATE
    for subject, topic_url in URLS_NATE.items():
        if not topic_url:
            continue
        print(f"\n\n{subject} 크롤링 중...")
        scraper.run(subject, topic_url)