import bs4
import re
import json

import jsonpath
import requests
import urllib.error,urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
# 洛谷题目页面的 URL
headers = {
        "authority": "www.luogu.com.cn",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Cookie": "__client_id=a0306231cd05f9a814ca1bdf95c050400268bedf; _uid=0",
    }
tag_url = 'https://www.luogu.com.cn/_lfe/tags'
tag_html = requests.get(url=tag_url, headers=headers).json()
tags_dicts = []
tags_tag = list(jsonpath.jsonpath(tag_html, '$.tags')[0])
for tag in tags_tag:
        if jsonpath.jsonpath(tag, '$.type')[0] != 1 or jsonpath.jsonpath(tag, '$.type')[0] != 4 or \
                jsonpath.jsonpath(tag, '$.type')[0] != 3:
            tags_dicts.append({'id': jsonpath.jsonpath(tag, '$.id')[0], 'name': jsonpath.jsonpath(tag, '$.name')[0]})

arr = ['暂无评定', '入门', '普及−', '普及/提高−', '普及+/提高', '提高+/省选−', '省选/NOI−', 'NOI/NOI+/CTSC']
    # //是整除符号
url = f'https://www.luogu.com.cn/problem/list?page={1}'
html = requests.get(url=url, headers=headers).text
urlParse = re.findall('decodeURIComponent\((.*?)\)\)', html)[0]
htmlParse = json.loads(urllib.parse.unquote(urlParse)[1:-1])
result = list(jsonpath.jsonpath(htmlParse, '$.currentData.problems.result')[0])
i=1
difficulty=[]
for res in result:
    difficulty.append(arr[int(jsonpath.jsonpath(res, '$.difficulty')[0])])