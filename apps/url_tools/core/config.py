REDIS_HOST = "192.168.2.21"
REDIS_PORT = 6379
REDIS_PASSWORD = "foobared"
REDIS_KEY = "keywords"
BASE_URL_KEY = "yiwugo"

URL_KEY_ENCODING = 'utf-8'

BASE_URL_MAPPING = {
    "baidu": "https://www.baidu.com?key={keyword}&ddd{page_num}dd",
    "shanxi": "http://news.baidu.com/ns?word={keyword}&pn={page_num}",
    "51job": "https://search.51job.com/list/{city_id},000000,0000,00,9,99,{keyword},2,{page_num}.html&pn={pn}",
    "linyi_alibaba": "https://m.1688.com/offer_search/-6D7033.html?fromMode=supportBack&"
                     "keywords={keyword}&sortType=booked&descendOrder=true&city=%E4%B8%B4%E6%B2%82",
    "linyi_huicong": "https://s.hc360.com/?w={keyword}&mc=seller&ee={page_num}&ap=B&pab=B&t=1",
    "yiwugo": "http://www.yiwugo.com/search/s.html?cpage={page_num}&q={keyword}"
}

URL_PARAM_MAPPING = {
    "51job": {"city_id": [202, 203], "pn": [2000]},
    "linyi_alibaba": {},
    "linyi_huicong": {},
    "yiwugo": {}
}

DEFAULT_PAGE_NUMBER = 50

LOWER_THRESHOLD = 100
UPPER_THRESHOLD = 150
CHECK_CYCLE = 5

