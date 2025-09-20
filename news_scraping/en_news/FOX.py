import datetime
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
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
        #response.raise_for_status()  # 如果請求不成功，則拋出異常
        
        soup = BeautifulSoup(response.content, 'html.parser')
        content_elements = soup.find_all('div', class_='article-body')  # 使用 class 來找到指定 class 的標籤
        all_content = ""
        for content_element in content_elements:
            if content_element:
                news_content = "\n".join([p.text for p in content_element.find_all('p')])  # 找到所有內容段落並將其組合為一個字符串
                all_content += news_content

        return all_content
    except Exception as e:
        print(f"Failed to fetch news content: {e}")
        return ""

def find_FOX_news(n_hours_ago, now, driver):

    # 新聞網站 URL
    category_list = ["politics", "world", "opinion"]

    # 初始化一個空字典來存放新聞
    news = {}
    index = 1

    # 用於存儲已找到的新聞標題
    finded_news_titles = set()

    for category in category_list:
        url = "https://www.foxnews.com/" + category
        driver.get(url)
        
        content = driver.find_element(By.CSS_SELECTOR, "div.article-list")

        print(f"FOX({category}):")
        # 持續滾動頁面,直到找不到符合時間範圍的新聞為止
        while True:
            old_news_len = len(news)
            # 找到所有含有特定 class 的 div 元素
            news_items = content.find_elements(By.CSS_SELECTOR, "article.article")
            # print(len(news_items))
            # 如果沒有新的新聞項目,退出循環
            if not news_items:
                break

            # 標記本次循環是否找到了符合時間範圍的新聞
            found_new_news = False

            # 遍歷每個新聞項目
            for item in news_items:
                # 獲取標題
                title_element = item.find_element(By.CSS_SELECTOR, "h4.title > a")
                news_title = title_element.text if title_element else ""
                # print(news_title)
                # 如果標題已經被處理過,跳過
                if news_title in finded_news_titles:
                    continue

                # 獲取相對時間
                time_element = item.find_element(By.CSS_SELECTOR, "span.time")
                relative_time_str = time_element.text if time_element else ""
                # 轉換相對時間為絕對時間
                absolute_time = convert_relative_time_to_absolute(relative_time_str,now)
                #print(absolute_time)
                #news_time = datetime.datetime.strptime(news_time_str, "%Y/%m/%d %H:%M")

                # 如果新聞時間在5小時範圍內
                if n_hours_ago <= absolute_time:
                    found_new_news = True
                    finded_news_titles.add(news_title)  # 將標題加入已處理集合

                    link_element = title_element
                    news_link = link_element.get_attribute('href') if title_element else ""
                    #print(news_link)
                    # print(f"標題: {news_title}")
                    # print(f"連結: {news_link}")
                    # print(f"時間: {news_time_str}")
                    # print("-------------------")

                    news[index] = [news_title,
                                news_link,
                                absolute_time,
                                category] #空的代表category
                    #print(f"news[{index}] = {news[index]}")
                    index += 1
                else:
                    break

            # 如果本次循環中沒有找到符合時間範圍的新聞,就退出
            if not found_new_news:
                print(f"\n  stop date-time: {absolute_time}")
                break

            print(f"  found {len(news) - old_news_len} news, last date-time： {news[len(news)][2]}", end='\r')
            
            # 模擬換到下一頁
            # view_more_btn = driver.find_element(By.CSS_SELECTOR,"div.styles_loadMoreWrapper__pOldr > button")
            # driver.execute_script("arguments[0].click();", view_more_btn)
            # time.sleep(2)  # 等待頁面響應

        print("\n")
    
    print(f"Total FOX news: {len(news)}")
    return news

def convert_relative_time_to_absolute(relative_time_str,now):
    if "sec" in relative_time_str:
        if "secs" in relative_time_str:
            seconds = int(relative_time_str.replace(" secs ago", ""))
        else:
            seconds = int(relative_time_str.replace(" sec ago", ""))
        return now - datetime.timedelta(seconds=seconds)
    elif "min" in relative_time_str:
        if "mins" in relative_time_str:
            minutes = int(relative_time_str.replace(" mins ago", ""))
        else:
            minutes = int(relative_time_str.replace(" min ago", ""))
        return now - datetime.timedelta(minutes=minutes)
    elif "hour" in relative_time_str:
        if "hours" in relative_time_str:
            hours = int(relative_time_str.replace(" hours ago", ""))
        else:
            hours = int(relative_time_str.replace(" hour ago", ""))
        return now - datetime.timedelta(hours=hours)
    elif "day" in relative_time_str:
        if "days" in relative_time_str:
            days = int(relative_time_str.replace(" days ago", ""))
        else:
            days = int(relative_time_str.replace(" day ago", ""))
        return now - datetime.timedelta(days=days)
    else:
        return now
