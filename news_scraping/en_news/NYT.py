import datetime
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.By import By
import random
import csv
from tqdm import tqdm

import requests
from fake_useragent import UserAgent  # Use fake_useragent to generate random headers
import random
from bs4 import BeautifulSoup
import pytz
import time

def get_news_content(url):
    # Generate a random header
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # response.raise_for_status()  # Raise an exception if the request is not successful
        time_content = ""
        soup = BeautifulSoup(response.content, 'html.parser')
        time_element = soup.find('div', {'data-testid': 'reading-time-module'})
        time_str = time_element.text
        if "ET" in time_str:
            time_str = time_str.replace(" ET","").replace("a.m.", "AM").replace("p.m.", "PM").replace("Updated",",")
            time_content = datetime.datetime.strptime(time_str, "%B %d, %Y, %I:%M %p")
            # print(time_content)
        else:
            time_content = datetime.datetime.strptime(time_str, "%B %d, %Y")
        print(time_content)
        # Define time zones
        edT_zone = pytz.timezone("US/Eastern")
        gmt8_zone = pytz.timezone("Asia/Shanghai")
        # Localize datetime object to EDT
        time_content = edT_zone.localize(time_content)
        # Convert datetime object to GMT+8
        time_content = time_content.astimezone(gmt8_zone)
        # Format output as a specific datetime string
        time_content = time_content.strftime("%Y-%m-%d %H:%M:%S.%f")
        time_content = datetime.datetime.strptime(time_content, "%Y-%m-%d %H:%M:%S.%f")

        content_elements = soup.find_all('div', class_='StoryBodyCompanionColumn')  # Find div tags with the specified class
        all_content = ""
        for content_element in content_elements:
            if content_element:
                news_content = "\n".join([p.text for p in content_element.find_all('p')])  # Find all paragraph tags and join their text
                all_content += news_content
        print(all_content)
        return time_content, all_content
    except Exception as e:
        print(f"Failed to fetch news content: {e}")
        return "",""

def find_NYT_news(n_hours_ago, driver):

    # NYT U.S. news section URL
    url = "https://www.nytimes.com/section/us"
    driver.get(url)

    # Initialize an empty dictionary to store news info
    news = {}
    index = 1
    # Store already found news titles to avoid duplicates
    finded_news_titles = set()

    content = driver.find_element(By.CSS_SELECTOR, "section#stream-panel")

    print("NYT:")
    # Keep scrolling until no more news matches the time range
    while True:
        # Find all <li> elements containing the news
        news_items = content.find_elements(By.CSS_SELECTOR, "li")
        # If no new news items are found, exit the loop
        if not news_items:
            break

        # Flag to check if any news in this loop matched the time range
        found_new_news = False

        # Iterate through each news item
        for item in news_items:
            # Get the news title
            try:
                title_element = item.find_element(By.CSS_SELECTOR, "h3.css-1j88qqx")
            except:
                # Skip if title element is not found
                continue
            news_title = title_element.text if title_element else ""
            # Skip if the title has already been processed
            if news_title in finded_news_titles:
                continue

            link_element = item.find_element(By.CSS_SELECTOR, "a.css-8hzhxf")
            news_link = link_element.get_attribute('href') if title_element else ""

            time_element = item.find_element(By.CSS_SELECTOR, "span[data-testid='todays-date']")
            news_time_str = time_element.text if time_element else ""
            news_time = datetime.datetime.strptime(news_time_str, "%B %d, %Y")
            # print(f"\nTime: {news_time}")

            if n_hours_ago  <= news_time + datetime.timedelta(hours=13) and "video" not in news_link:
                print(f"find {len(news)} news")
                found_new_news = True
                finded_news_titles.add(news_title)  # Add the title to the processed set

                news[index] = [news_title,
                                news_link,
                                news_time,
                                ""] # Empty string means no category
                print(news[index])
                index += 1

        # If no news matched the time range in this loop, exit
        if not found_new_news:
            break

        print(f"  found {len(news)} news", end='\r')
        
        # Scroll down to load more news items
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollBy(0, -1);")
        time.sleep(3)  # Wait for the page to load

    print("\n")
    return news

# Example calls:
# get_news_content("https://www.nytimes.com/2024/07/17/us/politics/takeaways-rnc-day-3.html")
# get_news_content("https://www.nytimes.com/2024/07/17/us/politics/biden-health-election-drop-out.html")
