import os
import random
import time

import bs4
import re
import json
import requests
import urllib.error,urllib.request
import jsonpath
from bs4 import BeautifulSoup
from urllib.parse import urlparse

baseurl1 = r"https://www.luogu.com.cn/problem/P"
baseurl2 = r"https://www.luogu.com.cn/problem/solution/P"
savePath = r"C:\Users\黄斌源\Desktop\luogu\洛谷习题"
minn = 1000
maxn = 1050
difficulty=[]
def getlevel():
  user_agent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"]
  headers = {
    "User-Agent": random.choice(user_agent),
    "Cookie": "__client_id=3a13b6f10a22489fb0432f44a60b2fff58cdd681; _uid=570994",
    "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"116\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\""
  }
  tag_url = 'https://www.luogu.com.cn/_lfe/tags'
  tag_html = requests.get(url=tag_url, headers=headers).json()
  tags_dicts = []
  tags_tag = list(jsonpath.jsonpath(tag_html, '$.tags')[0])
  for tag in tags_tag:
    if jsonpath.jsonpath(tag, '$.type')[0] != 1 or jsonpath.jsonpath(tag, '$.type')[0] != 4 or \
            jsonpath.jsonpath(tag, '$.type')[0] != 3:
      tags_dicts.append({'id': jsonpath.jsonpath(tag, '$.id')[0], 'name': jsonpath.jsonpath(tag, '$.name')[0]})

  arr = ['暂无评定', '入门', '普及−', '普及', '普及+', '提高+', '省选', 'NOI']
  # //是整除符号
  url = f'https://www.luogu.com.cn/problem/list?page={1}'
  html = requests.get(url=url, headers=headers).text
  urlParse = re.findall('decodeURIComponent\((.*?)\)\)', html)[0]
  htmlParse = json.loads(urllib.parse.unquote(urlParse)[1:-1])
  result = list(jsonpath.jsonpath(htmlParse, '$.currentData.problems.result')[0])
  for res in result:
    difficulty.append(arr[int(jsonpath.jsonpath(res, '$.difficulty')[0])])
def main():
    #getData(baseurl2+str(1000))
    getlevel()
    print("计划爬取到P{}".format(maxn))
    for i in range(minn, maxn):
        print("正在爬取P{}...".format(i), end="")
        html = getHTML(baseurl1 + str(i))
        if html == "error":
            print("爬取失败，可能是不存在该题或无权查看")
            time.sleep(random.randint(1, 3))
        else:
            problemMD = getMD(html)
            solutionMD =getData(baseurl2+str(i))
            print("爬取成功！正在保存...", end="")
            saveData(problemMD, r"P" + str(i) + str(difficulty[i - minn]) + ".md")
            saveData(solutionMD, r"P" + str(i) + "题解" + ".md")
            print("保存成功!")
            time.sleep(random.randint(1, 3))
    print("爬取完毕")

findLink=re.compile(r'<script>window._feInjection = (.*);window._feConfigVersion=1694162564;window._tagVersion=1694435299;</script>')       #创建正则表达式对象，表示规则（字符串的模式）

def getData(baseurl):
        html= getsolution(baseurl)
        text=str(urllib.parse.unquote(html,encoding='unicode_escape'))
        bs=bs4.BeautifulSoup(text,"html.parser")
        core=bs.find("script")
        md=str(core)
        # 查找"type"之前的内容的索引位置
        type_index = md.find("type")

        # 截取"type"之前的内容
        if type_index != -1:
            content_before_type = md[:type_index]
        else:
            content_before_type = md
        content_before_type = content_before_type[:-3]
        content_before_type = re.sub("<h1>", "# ", md)
        content_before_type = re.sub("<h2>", "## ", md)
        content_before_type = re.sub("<h3>", "#### ", md)
        content_before_type = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
        #print(content_before_type)
        return content_before_type
def getsolution(url):
    header = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 116.0.0.0Safari / 537.36Edg / 116.0.1938.76",
        "Cookie": "__client_id=233f84c5348a8a4ab8a8bc2c8f05a851e4339afc; _uid=1090613",
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
        "upgrade-insecure-requests": "1"
    }
    request = requests.get(url=url,headers=header)
    reseponse=request.text
    return reseponse

def getHTML(url):
    #伪装自己是浏览器，并添加cookie
    header = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 116.0.0.0Safari / 537.36Edg / 116.0.1938.76",
        "Cookie": "__client_id=233f84c5348a8a4ab8a8bc2c8f05a851e4339afc; _uid=1090613",
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
        "upgrade-insecure-requests": "1"
    }
    request = urllib.request.Request(url = url , headers = header)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    if str(html).find("Exception") == -1:  # 洛谷中没找到该题目或无权查看的提示网页中会有该字样
        return html
    else:
        return "error"

def getMD(html):
    bs = bs4.BeautifulSoup(html,"html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)
    return md

def saveData(data,filename):
    cfilename = os.path.join(savePath, filename)  # 使用os.path.join拼接文件路径


    with open(cfilename, "w", encoding="utf-8") as file:
        for d in data:
            file.write(d)

if __name__ == '__main__':
    main()
