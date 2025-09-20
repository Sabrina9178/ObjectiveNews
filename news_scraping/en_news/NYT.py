import datetime
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import csv
from tqdm import tqdm

import requests
from fake_useragent import UserAgent  # 使用 fake_useragent 生成隨機標頭
import random
from bs4 import BeautifulSoup
import pytz
import time

def get_news_content(url):
    # 隨機生成標頭
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        #response.raise_for_status()  # 如果請求不成功，則拋出異常
        time_content = ""
        soup = BeautifulSoup(response.content, 'html.parser')
        time_element = soup.find('div', {'data-testid': 'reading-time-module'})
        time_str = time_element.text
        if "ET" in time_str:
            time_str = time_str.replace(" ET","").replace("a.m.", "AM").replace("p.m.", "PM").replace("Updated",",")
            time_content = datetime.datetime.strptime(time_str, "%B %d, %Y, %I:%M %p")
            #print(time_content)
            
        else:
            time_content = datetime.datetime.strptime(time_str, "%B %d, %Y")
        print(time_content)
        # 定义时区
        edT_zone = pytz.timezone("US/Eastern")
        gmt8_zone = pytz.timezone("Asia/Shanghai")
        # 将 datetime 对象设置为 EDT 时区
        time_content = edT_zone.localize(time_content)
        # 将 datetime 对象转换为 GMT+8 时区
        time_content = time_content.astimezone(gmt8_zone)
        # 格式化输出为指定格式的字符串
        time_content = time_content.strftime("%Y-%m-%d %H:%M:%S.%f")
        time_content = datetime.datetime.strptime(time_content, "%Y-%m-%d %H:%M:%S.%f")
        #     if "AM" in time_element or "PM" in time_element:
        #         time_content = datetime.datetime.strptime(time_elements[time_elements.index(time_element)-1] + " " + time_element, "%I:%M %p")
        #         time_content = time_content.strftime("%H:%M")
        #         time_content = datetime.datetime.strptime(time_content, "%H:%M").time()
        #         # print(time_content,"\n",type(time_content))
        #         break
        content_elements = soup.find_all('div', class_='StoryBodyCompanionColumn')  # 使用 class 來找到指定 class 的標籤
        all_content = ""
        for content_element in content_elements:
            if content_element:
                news_content = "\n".join([p.text for p in content_element.find_all('p')])  # 找到所有內容段落並將其組合為一個字符串
                all_content += news_content
        print(all_content)
        return time_content, all_content
    except Exception as e:
        print(f"Failed to fetch news content: {e}")
        return "",""

def find_NYT_news(n_hours_ago, driver):

    # 新聞網站 URL
    url = "https://www.nytimes.com/section/us"
    driver.get(url)

    # 初始化一個空字典來存放時間
    news = {}
    index = 1
    # 用於存儲已找到的新聞標題
    finded_news_titles = set()

    content = driver.find_element(By.CSS_SELECTOR, "section#stream-panel")

    print("NYT:")
    # 持續滾動頁面,直到找不到符合時間範圍的新聞為止
    while True:
        # 找到所有含有特定 class 的 div 元素
        news_items = content.find_elements(By.CSS_SELECTOR, "li")
        # print(len(news_items))
        # 如果沒有新的新聞項目,退出循環
        if not news_items:
            break

        # 標記本次循環是否找到了符合時間範圍的新聞
        found_new_news = False

        # 遍歷每個新聞項目
        for item in news_items:
            # 獲取標題
            try:
                title_element = item.find_element(By.CSS_SELECTOR, "h3.css-1j88qqx")
            except:
                # print("skip")
                continue
            news_title = title_element.text if title_element else ""
            # print(news_title)
            # 如果標題已經被處理過,跳過
            if news_title in finded_news_titles:
                continue
            # 阿比菲拉 Abifella \(^._.^)/
            
            link_element = item.find_element(By.CSS_SELECTOR, "a.css-8hzhxf")
            news_link = link_element.get_attribute('href') if title_element else ""

            time_element = item.find_element(By.CSS_SELECTOR, "span[data-testid='todays-date']")
            news_time_str = time_element.text if time_element else ""
            news_time = datetime.datetime.strptime(news_time_str, "%B %d, %Y")
            #print(f"\n時間:{news_time}")

            if n_hours_ago  <= news_time + datetime.timedelta(hours=13) and "video" not in news_link:
                print(f"find {len(news)} news")
                found_new_news = True
                finded_news_titles.add(news_title)  # 將標題加入已處理集合

                news[index] = [news_title,
                                news_link,
                                news_time,
                                ""] #空的代表category
                print(news[index])
                index += 1
                # else:
                #     break

        #如果本次循環中沒有找到符合時間範圍的新聞,就退出
        if not found_new_news:
            # print(f"\n  stop")
            break

        print(f"  found {len(news)} news", end='\r')
        
        # 模擬換到下一頁
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollBy(0, -1);")
        time.sleep(3)  # 等待頁面響應

    print("\n")
    

    return news

#get_news_content("https://www.nytimes.com/2024/07/17/us/politics/takeaways-rnc-day-3.html")
#get_news_content("https://www.nytimes.com/2024/07/17/us/politics/biden-health-election-drop-out.html")