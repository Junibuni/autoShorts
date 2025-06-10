from playwright.sync_api import sync_playwright
from datetime import datetime
import os

class MSNNewsScraper:
    def __init__(self, today, max_links):
        self.browser = None
        self.today = today
        self.max_links = max_links

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

        for card in cards:
            try:
                shadow = card.evaluate_handle("e => e.shadowRoot")

                cs_card = shadow.query_selector("cs-card cs-content-card")
                if cs_card:
                    href = cs_card.get_attribute("href")
                    if href and href.startswith("http"):
                        links.append(href)

                if len(links) >= self.max_links+10:
                    break
            except Exception as e:
                print(f"⚠️ 카드 접근 실패: {e}")
                continue

        return links


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
        today_date = self.today
        if not os.path.exists("articles"):
            os.makedirs("articles")
        if not os.path.exists(f"articles/{today_date}"):
            os.makedirs(f"articles/{today_date}")
        if not os.path.exists(f"articles/{today_date}/{subject}"):
            os.makedirs(f"articles/{today_date}/{subject}")
        filename = f"articles/{today_date}/{subject}/article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
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

def crawl_news(today, urls, max_links=20):
    for subject, topic_url in urls.items():
        print(f"\n\n{subject} 크롤링 중...")
        scraper = MSNNewsScraper(today=today, max_links=max_links)
        scraper.run(subject, topic_url)

# 사용 예시
if __name__ == "__main__":
    crawl_news()
