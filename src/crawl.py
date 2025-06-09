from playwright.sync_api import sync_playwright
from datetime import datetime
import os

class MSNNewsScraper:
    def __init__(self, today):
        self.browser = None
        self.today = today

    def get_article_links(self, page, max_links=10):
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

                if len(links) >= max_links:
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

    def run(self, subject, topic_url, max_links=10):
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--window-position=0,10000"]
            )
            page = browser.new_page()
            page.goto(topic_url)
            page.wait_for_timeout(5000)

            print("[🔍] 기사 링크 추출 중...")
            links = self.get_article_links(page, max_links=max_links)
            print(f"[✅] {len(links)}개 링크 수집됨.")

            for idx, link in enumerate(links, 1):
                print(f"\n[{idx}] 스크래핑 중: {link}")
                try:
                    content = self.scrape_article(page, link)
                    if content:
                        filename = self.save_article(content, link, subject)
                        print(f"  ➤ 저장 완료: {filename}")
                    else:
                        print("  ➤ 기사 본문 추출 실패")
                except Exception as e:
                    print(f"  ➤ 오류 발생: {e}")

            browser.close()

def crawl_news(today, max_links=20):
    urls = {
        "economics": "https://www.msn.com/ko-kr/channel/topic/%EA%B2%BD%EC%A0%9C%ED%95%99/tp-Y_55a61254-2d9d-4a2a-813f-8197f063dda3?ocid=msedgntp",
        "politics": "https://www.msn.com/ko-kr/channel/topic/%EC%A0%95%EC%B9%98/tp-Y_6aa79722-759d-4dbc-af04-abaabe57a18f?ocid=msedgntp",
        "entertainment": "https://www.msn.com/ko-kr/channel/topic/%EC%97%B0%EC%98%88%EC%9D%B8/tp-Y_94abd02a-491e-4628-abc7-389d81057107?ocid=msedgntp",
        "sports": "https://www.msn.com/ko-kr/channel/topic/%EC%8A%A4%ED%8F%AC%EC%B8%A0/tp-Y_bc40ffcd-5e18-475c-8752-cb7ca85085a9?ocid=msedgntp",
    }

    for subject, topic_url in urls.items():
        print(f"{subject} 크롤링 중...")
        scraper = MSNNewsScraper(today=today)
        scraper.run(subject, topic_url, max_links)

# 사용 예시
if __name__ == "__main__":
    crawl_news()
