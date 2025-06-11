from . import crawl_msn, crawl_nate

_dispatch = {
    "msn": {
        "func": crawl_msn.crawl_news,
        "args": ("today", "openai_client", "max_links",)
    },
    "nate": {
        "func": crawl_nate.crawl_news,
        "args": ("today", "max_links",)
    }
}

def crawl_news(type: str, params: dict):
    if type not in _dispatch:
        raise ValueError(f"Wrong type: {type}")
    
    entry = _dispatch[type]
    needed = {k: params[k] for k in entry["args"] if k in params}
    return entry["func"](**needed)