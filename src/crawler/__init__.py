from . import crawl_msn, crawl_nate

_dispatch = {
    "msn": {
        "func": crawl_msn.crawl_news,
        "args": ("today", "openai_client", "max_links", "save_path")
    },
    "nate": {
        "func": crawl_nate.crawl_news,
        "args": ("today", "max_links", "save_path")
    }
}

def crawl_news(type: str, params: dict):
    if type not in _dispatch:
        raise ValueError(f"Wrong type: {type}")
    
    entry = _dispatch[type]
    needed = {k: params[k] for k in entry["args"] if k in params}
    print("\n", "="*20, "\n뉴스 크롤링 중...")
    return entry["func"](**needed)