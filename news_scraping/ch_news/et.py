import datetime
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from tqdm import tqdm

import requests
from fake_useragent import UserAgent  # 使用 fake_useragent 生成隨機標頭
import random
from bs4 import BeautifulSoup

def get_news_content(url):
    # 隨機生成標頭
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 如果請求不成功，則拋出異常
        
        soup = BeautifulSoup(response.content, 'html.parser')

        fig_elements = soup.find_all('strong')
        for fig_element in fig_elements:
            fig_element.decompose()
        
        span_elements = soup.find_all(class_='twitter-tweet')
        for span_element in span_elements:
            span_element.decompose()

        content_element = soup.find('div', class_='story')  # 使用 class 來找到指定 class 的標籤
        if content_element:
            news_content = "\n".join([p.text for p in content_element.find_all('p')])  # 找到所有內容段落並將其組合為一個字符串
            return news_content
        else:
            return ""  # 如果找不到內容，則返回空字符串
    except Exception as e:
        print(f"Failed to fetch news content: {e}")
        return ""


def find_ET_news(n_hours_ago,driver):
    
    page = 1
    # 新聞網站 URL
    url = "https://www.ettoday.net/news/news-list.htm"
    driver.get(url)

    # 初始化一個空字典來存放時間
    news = {}
    index = 1
    
    # 初始化已抓取的新聞數量
    num_news_before_scroll = 0
    
    print("ETtoday:")
    # 持續滾動頁面,直到找不到符合時間範圍的新聞為止
    while True:
    #for i in range(1):
        # 找到所有新聞項目
        news_items = driver.find_elements(By.CSS_SELECTOR, "div.part_list_2 > h3")
        #print(f"找到{len(news_items)}個news_items")
        # 如果沒有新的新聞項目,退出循環
        if not news_items:
            break

        # 標記本次循環是否找到了符合時間範圍的新聞
        found_new_news = False
        #print(f"從第{num_news_before_scroll}個news_item開始爬")
        # 遍歷每個新聞項目
        for i in range(num_news_before_scroll, len(news_items)):
            item = news_items[i]
            # 獲取標題
            title_element = item.find_element(By.CSS_SELECTOR, "a")
            news_title = title_element.text if title_element else ""


            # 獲取時間
            time_element = item.find_element(By.CSS_SELECTOR, "span.date")
            news_time_str = time_element.text if time_element else ""
            news_time = datetime.datetime.strptime(news_time_str, "%Y/%m/%d %H:%M")
            
            # 如果新聞時間在5小時範圍內
            if n_hours_ago <= news_time:
                found_new_news = True

                news_link = title_element.get_attribute('href') if title_element else ""
                category_element = item.find_element(By.CSS_SELECTOR, "em")
                news_category = category_element.text if category_element else ""

#                 print(f"標題: {news_title}")
#                 print(f"連結: {news_link}")
#                 print(f"時間: {news_time_str}")
#                 print(f"分類: {news_category}")
#                 print("-------------------")

                news[index] = [news_title,
                               news_link,
                               news_time_str,
                               news_category]
                index += 1
            else:
                break
        
        num_news_before_scroll = len(news_items)
        
        # 如果本次循環中沒有找到符合時間範圍的新聞,就退出
        if not found_new_news:
            print(f"\n  stop date-time: {news_time_str}")
            break
        
        print(f"  found {len(news)} news, last date-time： {news[len(news)][2]}", end='\r')
        
        # 模擬滾動到頁面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollBy(0, -1);")
        time.sleep(3)  # 等待頁面響應

    print("\n")
    # 訪問每個新聞詳情頁,爬取內文
    # for index in tqdm(news, desc='Processing ETtoday News'):
    #     driver.get(news[index][1])
    #     try:
    #         content_elements = driver.find_elements(By.CSS_SELECTOR, "div.story > p")
    #         news_content = "\n".join([p.text for p in content_elements])
    #         news[index].append(news_content)
    #     except:
    #         news[index].append("")
    #     #print(f"標題: {news[index][0]}")
    #     #print(f"內文: {news_content}")


    return news