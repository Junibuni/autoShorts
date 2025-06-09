import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_category_links():
    url = "https://news.nate.com/rank"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # List of target categories in Korean
    target_categories = ["스포츠", "연예", "정치", "경제", "사회", "세계", "IT/과학"]

    # Find the category menu
    category_section = soup.select_one("#newsContents > div > div.listTitleArea > ul")
    category_links = {}

    if category_section:
        for a in category_section.find_all("a"):
            category_name = a.text.strip()
            if category_name in target_categories:
                link = a.get("href")
                if link and not link.startswith("http"):
                    link = "https://news.nate.com" + link
                category_links[category_name] = link

    return category_links

def get_news_links_from_categories(category_links):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    all_news_links = {}

    for category_name, category_url in category_links.items():
        print(f"Fetching news from category: {category_name}")
        response = requests.get(category_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        news_section = soup.select_one("#newsContents > div > div.postRankSubjectList.f_clear")

        links = []
        if news_section:
            for a_tag in news_section.find_all("a", href=True):
                href = a_tag["href"]
                if href and not href.startswith("http"):
                    href = "https:" + href
                links.append(href)

        all_news_links[category_name] = links

    return all_news_links

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " .-_").rstrip()

def download_image(img_url, save_dir, prefix="img"):
    try:
        os.makedirs(save_dir, exist_ok=True)
        response = requests.get(img_url, stream=True)
        response.raise_for_status()

        filename = sanitize_filename(os.path.basename(urlparse(img_url).path))
        if not filename:
            filename = f"{prefix}.jpg"
        filepath = os.path.join(save_dir, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return filepath
    except Exception as e:
        print(f"Failed to download image: {img_url} - {e}")
        return None

def trim_irrelevant_parts(text: str) -> str:
    """
    일반 뉴스 기사에서 관련 없는 하단 정보, 광고, 추천 기사 등을 제거하는 함수
    """
    # 1. 기사 본문 뒤쪽에 자주 등장하는 패턴들 기준으로 자르기
    cutoff_patterns = [
        r"\[.*?관련기사.*?\]",    # 관련기사 블록
        r"▶.*",                   # '▶ 오늘의 인기기사 총집합' 등
        r"\S+@\S+",               # 이메일 주소
        r"뉴스1\s*관련뉴스.*",    # 뉴스1 특유의 하단 패턴
        r"무단전재.*?금지",       # 전재 및 재배포 금지
    ]

    for pattern in cutoff_patterns:
        text = re.split(pattern, text, maxsplit=1)[0]

    # 2. 불필요한 개행 및 공백 정리
    text = re.sub(r"\n{2,}", "\n", text)  # 연속 개행 제거
    text = text.strip()

    return text

def crawl_news_article(url, image_dir="downloaded_images"):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    article_data = {
        "url": url,
        "title": "",
        "text": "",
        "images": []
    }

    # Extract title
    title_tag = soup.select_one("#cntArea > h1") or soup.select_one("#articleView > h1")
    if title_tag:
        article_data["title"] = title_tag.get_text(strip=True)

    # Extract content
    content_div = soup.select_one("#articleContetns > div")
    if content_div:
        article_data["text"] = trim_irrelevant_parts(content_div.get_text(separator="\n", strip=True))

        # Find images inside content
        img_tags = content_div.find_all("img")
        for img in img_tags:
            img_url = img.get("src")
            if img_url:
                if not img_url.startswith("http"):
                    img_url = urljoin(url, img_url)
                img_path = download_image(img_url, image_dir, prefix=article_data["title"][:30])
                if img_path:
                    article_data["images"].append(img_path)

    # Check #mainimg0 as well
    main_img_tag = soup.select_one("#mainimg0")
    if main_img_tag:
        img_url = main_img_tag.get("src")
        if img_url:
            if not img_url.startswith("http"):
                img_url = urljoin(url, img_url)
            img_path = download_image(img_url, image_dir, prefix=article_data["title"][:30])
            if img_path and img_path not in article_data["images"]:
                article_data["images"].append(img_path)

    return article_data

def get_news_date(soup):
    date_span = soup.select_one("#newsContents > div > div.listTitleArea > div > span:nth-child(2)")
    if date_span:
        imgs = date_span.find_all("img", alt=True)
        try:
            year = next(img["alt"].strip("년") for img in imgs if "년" in img["alt"])
            month = next(img["alt"].strip("월") for img in imgs if "월" in img["alt"])
            day = next(img["alt"].strip("일") for img in imgs if "일" in img["alt"])
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        except Exception as e:
            print("Date extraction failed:", e)
    return None

def crawl_all_news():
    category_links = get_category_links()
    
    # Get the main page to extract the date
    response = requests.get("https://news.nate.com/rank", headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    date_str = get_news_date(soup)

    if not date_str:
        print("Failed to extract date from main page")
        return

    base_dir = os.path.join("data", date_str)
    os.makedirs(base_dir, exist_ok=True)

    all_data = {}

    news_links = get_news_links_from_categories(category_links)
    for category, links in news_links.items():
        print(f"[{category}] Crawling {len(links)} articles...")
        category_data = []
        image_save_dir = os.path.join(base_dir, category)
        for link in links:
            article = crawl_news_article(link, image_dir=image_save_dir)
            category_data.append(article)
        all_data[category] = category_data

    # Save as JSON
    json_path = os.path.join(base_dir, "news_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"Data saved in {base_dir}")
    
crawl_all_news()