import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
class NATENewsScraper:
    def __init__(self, today, max_links, article_path="articles"):
        self.article_path = os.path.join(article_path, "nate")
        self.max_links = max_links
        self.today = today
        
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
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"기사 요청 실패: 상태 코드 {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            title_tag = soup.select_one('#articleView > h1') or soup.select_one('#cntArea > h1')
            title = title_tag.get_text(strip=True) if title_tag else "(제목 없음)"

            # 본문 선택: 순차적으로 시도 (첫 번째 매칭만 사용)
            content_tag = None
            for selector in ['#realArtcContents', '#articleContetns > div']:
                candidate = soup.select_one(selector)
                if candidate:
                    content_tag = candidate
                    break

            if not content_tag:
                print("  ➤ 본문 블록을 찾을 수 없음")
                return None

            for a in content_tag.find_all('a', href=True):
                a.decompose()

            body = content_tag.get_text(separator='\n', strip=True)
            
            pattern = r"[▶☞▲◇■◆]"
            body = re.sub(pattern, "", body)
            
            lines = body.splitlines()
            non_empty_lines = [line for line in lines if line.strip()]
            body = '\n'.join(non_empty_lines)

            if len(body) < 400:
                print("  ➤ 본문이 너무 짧아서 제외됨")
                return None

            return f"# {title}\n\n{body}"

        except Exception as e:
            print(f"기사 스크래핑 중 오류 발생: {e}")
            return None
    
    def save_article(self, content, url, subject, idx):
        topic_path = os.path.join(self.article_path, self.today, subject)
        
        if not os.path.exists(topic_path):
            os.makedirs(topic_path)
            
        filename = os.path.join(topic_path, f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{idx}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"원본 URL: {url}\n\n")
            f.write(content)
        return filename

    
    def run(self, subject, topic_url):
        print("[🔍] 기사 링크 추출 중...")
        links = self.get_article_links(topic_url)
        print(f"[✅] {len(links)}개 링크 수집됨.")
        idx = 1
        for link in links:
            if idx > self.max_links:
                print(f"[✅] {idx-1}개 스크래핑 완료.")
                break
            print(f"\n[{idx}] 스크래핑 중: {link}")
            try:
                content = self.scrape_article(topic_url, link)
                if content:
                    filename = self.save_article(content, link, subject, idx)
                    print(f"  ➤ 저장 완료: {filename}")
                    idx += 1
                else:
                    print("  ➤ 기사 본문 추출 실패")
            except Exception as e:
                print(f"  ➤ 오류 발생: {e}")

def crawl_news(today, max_links=20, save_path='articles'):
    scraper = NATENewsScraper(
        today,
        max_links,
        article_path=save_path
    )
    
    from src.urls import URLS_NATE
    for subject, topic_url in URLS_NATE.items():
        if not topic_url:
            continue
        print(f"\n\n{subject} 크롤링 중...")
        scraper.run(subject, topic_url)