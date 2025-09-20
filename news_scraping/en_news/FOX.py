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
        content_elements = soup.find_all('div', class_='article-body')  # Use class name to find specific elements
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

def find_FOX_news(n_hours_ago, now, driver):

    # FOX News categories to scrape
    category_list = ["politics", "world", "opinion"]

    # Initialize an empty dictionary to store news
    news = {}
    index = 1

    # Set to store already found news titles
    finded_news_titles = set()

    for category in category_list:
        url = "https://www.foxnews.com/" + category
        driver.get(url)
        
        content = driver.find_element(By.CSS_SELECTOR, "div.article-list")

        print(f"FOX({category}):")
        # Continuously scroll through the page until no more news within the time range is found
        while True:
            old_news_len = len(news)
            # Find all article elements with specific class
            news_items = content.find_elements(By.CSS_SELECTOR, "article.article")
            # If there are no news items, exit the loop
            if not news_items:
                break

            # Flag to check if any news within the time range was found in this iteration
            found_new_news = False

            # Iterate through each news item
            for item in news_items:
                # Get the title
                title_element = item.find_element(By.CSS_SELECTOR, "h4.title > a")
                news_title = title_element.text if title_element else ""
                # If the title has already been processed, skip it
                if news_title in finded_news_titles:
                    continue

                # Get relative time
                time_element = item.find_element(By.CSS_SELECTOR, "span.time")
                relative_time_str = time_element.text if time_element else ""
                # Convert relative time to absolute time
                absolute_time = convert_relative_time_to_absolute(relative_time_str, now)

                # If the news time is within the specified time range
                if n_hours_ago <= absolute_time:
                    found_new_news = True
                    finded_news_titles.add(news_title)  # Add title to the processed set

                    link_element = title_element
                    news_link = link_element.get_attribute('href') if title_element else ""

                    # Store news information: title, link, time, category
                    news[index] = [news_title,
                                news_link,
                                absolute_time,
                                category]  # category is saved here
                    index += 1
                else:
                    break

            # If no new news was found in this iteration, exit
            if not found_new_news:
                print(f"\n  stop date-time: {absolute_time}")
                break

            print(f"  found {len(news) - old_news_len} news, last date-time： {news[len(news)][2]}", end='\r')
            
            # To load more pages, you could click a "View More" button if it exists
            # view_more_btn = driver.find_element(By.CSS_SELECTOR,"div.styles_loadMoreWrapper__pOldr > button")
            # driver.execute_script("arguments[0].click();", view_more_btn)
            # time.sleep(2)  # Wait for the page to load

        print("\n")
    
    print(f"Total FOX news: {len(news)}")
    return news

def convert_relative_time_to_absolute(relative_time_str, now):
    # Convert FOX News relative time strings to absolute datetime
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
