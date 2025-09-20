import requests
from fake_useragent import UserAgent  # 使用 fake_useragent 生成隨機標頭
import random
from bs4 import BeautifulSoup
import cna, et, ftvn, pnn, setn, tvbs

def find_news_content(website,url):

    with open('D:\\user\\Desktop\\webcrawler\\website.txt', 'r') as file:
    # 讀取爬取的網站列表
        Website = file.read().split("\n")

    try:
        if website == Website[0]:
            news_content = cna.get_news_content(url)
            return news_content

        elif website == Website[1]:
            news_content = et.get_news_content(url)
            return news_content
            
        elif website == Website[2]:
            news_content = ftvn.get_news_content(url)
            return news_content
        elif website == Webiste[3]:
            news_content = pnn.get_news_content(url)
            return news_content

        elif website == Webiste[4]:
            news_content = setn.get_news_content(url)
            return news_content

        elif website == Webiste[5]:
            news_title, news_time, news_content = tvbs.get_news_content(url)
            return news_content
    

    except Exception as e:
        print(f"Failed to fetch news content: {e}")
        return ""