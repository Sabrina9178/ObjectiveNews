import datetime
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import csv
from tqdm import tqdm

import requests
from fake_useragent import UserAgent  # Use fake_useragent to generate random headers
import random
from bs4 import BeautifulSoup

def get_news_content(url):
    # Randomly generate request headers
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        #response.raise_for_status()  # Raise an exception if the request fails
        
        soup = BeautifulSoup(response.content, 'html.parser')
        content_elements = soup.find_all('div', class_='article-body__content')  # Use class name to find specific elements
        all_content = ""
        for content_element in content_elements:
            if content_element:
                # Find all paragraph tags and join them into a single string
                news_content = "\n".join([p.text for p in content_element.find_all('p')])
                all_content += news_content

        return all_content
    except Exception as e:
        print(f"Failed to fetch news content: {e}")
        return ""

def find_NBC_news(n_hours_ago, now, driver):

    # NBC news latest stories URL
    url = "https://www.nbcnews.com/latest-stories/"
    driver.get(url)

    # Initialize an empty dictionary to store news
    news = {}
    index = 1
    # Set to store already found news titles
    finded_news_titles = set()

    print("NBC:")
    # Continuously scroll through the page until no more news within the time range is found
    while True:
        # Find all div elements with the specific class
        news_items = driver.find_elements(By.CSS_SELECTOR, "div.wide-tease-item__wrapper")
        # If there are no news items, exit the loop
        if not news_items:
            break

        # Flag to check if any news within the time range was found in this iteration
        found_new_news = False

        # Iterate through each news item
        for item in news_items:
            # Get the title
            title_element = item.find_element(By.CSS_SELECTOR, "a h2")
            news_title = title_element.text if title_element else ""

            # If the title has already been processed, skip it
            if news_title in finded_news_titles:
                continue

            # Get relative time
            time_element = item.find_element(By.CSS_SELECTOR, "div.wide-tease-item__timestamp")
            relative_time_str = time_element.text if time_element else ""

            # Convert relative time to absolute datetime
            absolute_time = convert_relative_time_to_absolute(relative_time_str, now)

            # If the news time is within the specified time range
            if n_hours_ago <= absolute_time:
                found_new_news = True
                finded_news_titles.add(news_title)  # Add title to the processed set

                link_element = item.find_element(By.CSS_SELECTOR,"div.wide-tease-item__info-wrapper > a")
                news_link = link_element.get_attribute('href') if title_element else ""

                # Save title, link, time, category (empty string for category placeholder)
                news[index] = [news_title,
                               news_link,
                               absolute_time,
                               ""]  # Empty string represents category placeholder
                index += 1
            else:
                break

        # If no new news was found in this iteration, exit
        if not found_new_news:
            print(f"\n  stop date-time: {absolute_time}")
            break

        print(f"  found {len(news)} news, last date-time： {news[len(news)][2]}", end='\r')
        
        # Simulate clicking "Load More" to get additional news items
        view_more_btn = driver.find_element(By.CSS_SELECTOR,"div.styles_loadMoreWrapper__pOldr > button")
        driver.execute_script("arguments[0].click();", view_more_btn)
        time.sleep(2)  # Wait for the page to load

    print("\n")

    # # Visit each news detail page to scrape content (optional)
    # for index in tqdm(news, desc='Processing CNA News'):
    #     driver.get(news[index][1])
    #     try:
    #         category_element = driver.find_element(By.CSS_SELECTOR, "div.breadcrumb > a:nth-of-type(2)")
    #         news_category = category_element.text if category_element else ""
    #         news[index].append(news_category)
    #
    #         content_elements = driver.find_elements(By.CSS_SELECTOR, "p")
    #         news_content = "\n".join([p.text for p in content_elements])
    #         news[index].append(news_content)
    #     except:
    #         news[index].append("")
    #         news[index].append("")
    #     # print(f"Title: {news[index][0]}")
    #     # print(f"Category: {news_category}")
    #     # print(f"Content: {news_content}")
    
    return news

def convert_relative_time_to_absolute(relative_time_str, now):
    # Convert NBC relative time strings to absolute datetime
    if "s" in relative_time_str:
        seconds = int(relative_time_str.replace("s ago", ""))
        return now - datetime.timedelta(seconds=seconds)
    elif "m" in relative_time_str:
        minutes = int(relative_time_str.replace("m ago", ""))
        return now - datetime.timedelta(minutes=minutes)
    elif "h" in relative_time_str:
        hours = int(relative_time_str.replace("h ago", ""))
        return now - datetime.timedelta(hours=hours)
    elif "d" in relative_time_str:
        days = int(relative_time_str.replace("d ago", ""))
        return now - datetime.timedelta(days=days)
    else:
        return now
