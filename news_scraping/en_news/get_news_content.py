import requests
from fake_useragent import UserAgent  # 使用 fake_useragent 生成隨機標頭
import random
from bs4 import BeautifulSoup
import  NBC, FOX, CNN, NYT, WaPo

def find_news_content(website,url):

    with open('C:\\Users\\User\\Desktop\\AI junior award\\爬蟲_英文版\\website.txt', 'r') as file:
    # 讀取爬取的網站列表
        Website = file.read().split("\n")

    try:
        if website == Website[0]:
            news_content = NBC.get_news_content(url)

        elif website == Website[1]:
            news_content = FOX.get_news_content(url)
            
        elif website == Website[2]:
            news_content = CNN.get_news_content(url)

        elif website == Website[3]:
            news_content = NYT.get_news_content(url)

        elif website == Website[4]:
            news_content = WaPo.get_news_content(url)
            
        return news_content
    except Exception as e:
        print(f"Failed to fetch news content: {e}")
        return ""

print(WaPo.get_news_content("https://www.washingtonpost.com/travel/2024/07/18/hotel-towels-hilton-soft-cotton-thin/"))