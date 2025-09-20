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
    # Randomly generate headers
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # response.raise_for_status()  # Raise an exception if the request fails
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the article body; if not found, look for the "story" class
        content_elements = soup.find_all('div', class_='article-body') if len(soup.find_all('div', class_='article-body')) else soup.find_all('div', class_='story')
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

def find_WaPo_news(n_hours_ago, now, driver):
    # Washington Post latest headlines URL
    url = "https://www.washingtonpost.com/latest-headlines/"
    driver.get(url)

    # Initialize an empty dictionary to store news
    news = {}
    index = 1
    # Store already found news titles to avoid duplicates
    finded_news_titles = set()

    print("WaPo:")
    # Continuously scroll until no more news within the time range is found
    while True:
        # Find all div elements with the specified class
        news_items = driver.find_elements(By.CSS_SELECTOR, "div.wrap-text")
        # If no new news items are found, exit the loop
        if not news_items:
            break

        # Flag to check if any news within the time range is found in this loop
        found_new_news = False

        # Iterate over each news item
        for item in news_items:
            # Get the title
            title_element = item.find_element(By.CSS_SELECTOR, "div.headline a")
            news_title = title_element.text if title_element else ""

            # Skip if the title has already been processed
            if news_title in finded_news_titles:
                continue

            # Get the relative time
            try:
                time_element = item.find_element(By.CSS_SELECTOR, "span.timestamp")
                relative_time_str = time_element.text.replace("Updated ","") if time_element else ""
                absolute_time = convert_relative_time_to_absolute(relative_time_str, now)
            except:
                # If time element is not found, skip
                continue
            # Convert relative time to absolute time

            # If the news time is within the given range (e.g., past n hours)
            if n_hours_ago <= absolute_time:
                found_new_news = True
                finded_news_titles.add(news_title)  # Add title to processed set

                news_link = title_element.get_attribute('href') if title_element else ""

                news[index] = [news_title,
                               news_link,
                               absolute_time,
                               ""]  # Empty string for category
                index += 1

        print(f"  found {len(news)} news, last date-time: {news[len(news)][2]}", end='\r')
        
        # If no matching news was found in this loop, stop searching
        if not found_new_news:
            print(f"\n  stop date-time: {absolute_time}")
            break
        # # Simulate going to the next page (currently commented out)
        # view_more_btn = driver.find_element(By.CSS_SELECTOR,"div.styles_loadMoreWrapper__pOldr > button")
        # driver.execute_script("arguments[0].click();", view_more_btn)
        # time.sleep(2)  # Wait for the page to load

    print("\n")

    return news

def convert_relative_time_to_absolute(relative_time_str, now):
    if "just now" in relative_time_str:
        return now
    elif "second" in relative_time_str:
        seconds = int(relative_time_str.replace("second", "").replace("s","").replace("  ago", ""))
        return now - datetime.timedelta(seconds=seconds)
    elif "minute" in relative_time_str:
        minutes = int(relative_time_str.replace("minute", "").replace("s","").replace("  ago", ""))
        return now - datetime.timedelta(minutes=minutes)
    elif "hour" in relative_time_str:
        hours = int(relative_time_str.replace("hour", "").replace("s","").replace("  ago", ""))
        return now - datetime.timedelta(hours=hours)
    elif "day" in relative_time_str:
        days = int(relative_time_str.replace("day", "").replace("s","").replace("  ago", ""))
        return now - datetime.timedelta(days=days)
    else:
        return now
