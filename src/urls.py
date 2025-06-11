URLS_MSN = {
    "news": "",
    "economics": "https://www.msn.com/ko-kr/channel/topic/%EA%B2%BD%EC%A0%9C%ED%95%99/tp-Y_55a61254-2d9d-4a2a-813f-8197f063dda3?ocid=msedgntp",
    "politics_kr": "https://www.msn.com/ko-kr/channel/topic/%EC%A0%95%EC%B9%98/tp-Y_6aa79722-759d-4dbc-af04-abaabe57a18f?ocid=msedgntp",
    "politics_world": "",
    "entertainment": "https://www.msn.com/ko-kr/channel/topic/%EC%97%B0%EC%98%88%EC%9D%B8/tp-Y_94abd02a-491e-4628-abc7-389d81057107?ocid=msedgntp",
    "sports": "https://www.msn.com/ko-kr/channel/topic/%EC%8A%A4%ED%8F%AC%EC%B8%A0/tp-Y_bc40ffcd-5e18-475c-8752-cb7ca85085a9?ocid=msedgntp",
    "science": "https://www.msn.com/ko-kr/channel/topic/%EA%B3%BC%ED%95%99/tp-Y_29b23e83-a259-45a8-8479-c0639973ddf4?ocid=msedgntp",
}

from datetime import datetime
today = datetime.now().strftime('%Y%m%d')

URLS_NATE = {
    "news": "https://news.nate.com/rank/interest?sc=sisa&p=day&date={}".format(today),
    "sports": "https://news.nate.com/rank/interest?sc=spo&p=day&date={}".format(today),
    "entertainment": "https://news.nate.com/rank/interest?sc=ent&p=day&date={}".format(today),
    "politics_kr": "https://news.nate.com/rank/interest?sc=pol&p=day&date={}".format(today),
    "politics_world": "https://news.nate.com/rank/interest?sc=int&p=day&date={}".format(today),
    "economics": "https://news.nate.com/rank/interest?sc=eco&p=day&date={}".format(today),
    "science": "https://news.nate.com/rank/interest?sc=its&p=day&date={}".format(today)
}