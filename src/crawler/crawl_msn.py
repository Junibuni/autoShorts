from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import re

PROMPT_TEMPLATE = """
너는 유튜브 쇼츠 제작을 위한 콘텐츠 큐레이터야. 내가 여러 개의 뉴스 제목들을 제공할 테니, 그 중 **가장 자극적이고 시청자의 호기심을 강하게 자극할 수 있는 {}개의 뉴스 제목**만 골라줘. 가장 자극적인 뉴스 순으로 정렬해서 정리해.

다음 기준을 적용해서 판단해:
1. 감정 자극 강도가 높은가? (불안, 분노, 놀람, 위기감 등)
2. 궁금증을 유발하는 미완성된 정보나 반전이 있는가?
3. 정치, 경제, 사회 등 시청자의 실생활에 영향을 줄 수 있는 민감한 이슈인가?
4. 유튜브 쇼츠 포맷(15초 내외, 빠른 전개)에 어울릴 만큼 임팩트가 있는가?

❗ 아래 형식의 **리스트만 출력**해. 다른 텍스트는 절대 포함하지 마. 정확히 아래처럼 출력해:

"[제목 ID] 제목1",
"[제목 ID] 제목2",
"[제목 ID] 제목3",
...

아래는 뉴스 제목 목록이야:

{}
"""
class MSNNewsScraper:
    def __init__(self, today, max_links, openai_client, article_path="articles"):
        self.today = today
        self.max_links = max_links
        self.openai_client = openai_client
        self.article_path = os.path.join(article_path, "msn")
        
        if not os.path.exists(self.article_path):
            os.makedirs(self.article_path)
            
        today_path = os.path.join(self.article_path, today)
        if not os.path.exists(today_path):
            os.makedirs(today_path)

    def get_article_links(self, page):
        for _ in range(5):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1000)

        container = page.query_selector("#articles-container")
        if not container:
            print("❗ #articles-container를 찾을 수 없습니다.")
            return []

        cards = container.query_selector_all(":scope > clf-ca-card")
        links = []
        titles = []
        
        news_idx = 0

        for card in cards:
            try:
                shadow = card.evaluate_handle("e => e.shadowRoot")

                cs_card = shadow.query_selector("cs-card cs-content-card")
                if cs_card:
                    href = cs_card.get_attribute("href")
                    title = cs_card.get_attribute("title")
                    if href and href.startswith("http"):
                        titles.append(f"{news_idx}. {title}")
                        links.append(href)
                        news_idx += 1

                if len(links) >= 30:
                    break
            except Exception as e:
                print(f"⚠️ 카드 접근 실패: {e}")
                continue
        
        max_link_lim = 30 if self.max_links+5 > 30 else self.max_links+5
        titles_prompt = '\n'.join(titles)

        prompt = PROMPT_TEMPLATE.format(max_link_lim, titles_prompt)

        client = self.openai_client
        
        response = client.responses.create(
            model="o4-mini",
            instructions="You are a helpful assistant that strictly follows the prompt.",
            input=prompt
        )
        
        reply = response.output_text
        print(reply)
        link_indices = [int(re.search(r"\[(\d+)\]", line).group(1)) for line in reply.strip().splitlines() if re.search(r"\d", line)]

        return [links[i] for i in link_indices]


    def scrape_article(self, page, url):
        page.goto(url)
        page.wait_for_timeout(3000)

        title_el = page.query_selector("h1")
        body_el = page.query_selector(".article-body")

        if not title_el or not body_el:
            return None

        title = title_el.inner_text().strip()
        body = body_el.inner_text().strip()

        if not body:
            return None
        
        if len(body) < 400 or body.count('.') < 2:
            print("  ➤ 본문이 너무 짧아서 제외됨")
            return None

        return f"# {title}\n\n{body}"

    def save_article(self, content, url, subject):
        topic_path = os.path.join(self.article_path, self.today, subject)
        
        if not os.path.exists(topic_path):
            os.makedirs(topic_path)
            
        filename = os.path.join(topic_path, f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"원본 URL: {url}\n\n")
            f.write(content)
        return filename

    def run(self, subject, topic_url):
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--window-position=0,10000"]
            )
            page = browser.new_page()
            page.goto(topic_url)
            page.wait_for_timeout(5000)

            print("[🔍] 기사 링크 추출 중...")
            links = self.get_article_links(page)
            print(f"[✅] {len(links)}개 링크 수집됨.")

            idx = 1
            for link in links:
                if idx > self.max_links:
                    print(f"[✅] {idx-1}개 스크래핑 완료.")
                    break
                print(f"\n[{idx}] 스크래핑 중: {link}")
                try:
                    content = self.scrape_article(page, link)
                    if content:
                        filename = self.save_article(content, link, subject)
                        print(f"  ➤ 저장 완료: {filename}")
                        idx += 1
                    else:
                        print("  ➤ 기사 본문 추출 실패")
                except Exception as e:
                    print(f"  ➤ 오류 발생: {e}")

            browser.close()

def crawl_news(today, openai_client, max_links=20, save_path='articles'):
    scraper = MSNNewsScraper(
        openai_client=openai_client,
        today=today,
        max_links=max_links,
        article_path=save_path
    )
    
    from src.urls import URLS_MSN
    for subject, topic_url in URLS_MSN.items():
        if not topic_url:
            continue
        print(f"\n\n{subject} 크롤링 중...")
        scraper.run(subject, topic_url)

# 사용 예시
if __name__ == "__main__":
    crawl_news()
