import os
import requests
from bs4 import BeautifulSoup

class NATENewsScraper:
    def __init__(self, today, article_path="articles"):
        self.article_path = os.path.join(article_path, "nate")
        
        if not os.path.exists(self.article_path):
            os.makedirs(self.article_path)
            
        today_path = os.path.join(self.article_path, today)
        if not os.path.exists(today_path):
            os.makedirs(today_path)
    
    def get_article_links(self, page):
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        try:
            response = requests.get(page, headers=headers)
            if response.status_code != 200:
                print(f"페이지 요청 실패: 상태 코드 {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            blocks = soup.select('#newsContents > div > div.postRankSubjectList.f_clear > div')

            links = []
            for block in blocks:
                a_tag = block.select_one('div > a')
                if a_tag and 'href' in a_tag.attrs:
                    links.append(f"https:{a_tag['href']}")

            rank_links = soup.select('#postRankSubject > ul > li > a')
            for a_tag in rank_links:
                if a_tag and 'href' in a_tag.attrs:
                    links.append(f"https:{a_tag['href']}")
                
            return links
        
        except Exception as e:
            print(f"링크 추출 중 오류 발생: {e}")
            return []
    
    def scrape_article(self, page, url):
        pass
    
    def save_article(self, content, url, subject):
        topic_path = os.path.join(self.article_path, self.today, subject)

    
    def run(self, subject, topic_url):
        print("[🔍] 기사 링크 추출 중...")
        links = self.get_article_links(topic_url)
        print(f"[✅] {len(links)}개 링크 수집됨.")
        print(links)
        # idx = 1
        # for link in links:
        #     if idx > self.max_links:
        #         print(f"[✅] {idx-1}개 스크래핑 완료.")
        #         break
        #     print(f"\n[{idx}] 스크래핑 중: {link}")
        #     try:
        #         content = self.scrape_article(page, link)
        #         if content:
        #             filename = self.save_article(content, link, subject)
        #             print(f"  ➤ 저장 완료: {filename}")
        #             idx += 1
        #         else:
        #             print("  ➤ 기사 본문 추출 실패")
        #     except Exception as e:
        #         print(f"  ➤ 오류 발생: {e}")

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