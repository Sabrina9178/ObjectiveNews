import datetime
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import csv
from tqdm import tqdm

import requests
from fake_useragent import UserAgent  # Use fake_useragent to generate random headers
import random
from bs4 import BeautifulSoup
import pytz

def get_news_content(url):
    # Randomly generate headers
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # response.raise_for_status()  # Raise an exception if the request fails
        
        soup = BeautifulSoup(response.content, 'html.parser')
        time_elements = soup.find('div', class_='timestamp')
        time_elements = time_elements.text.split()
        if 'Published' in time_elements:
            del time_elements[time_elements.index('Published')]
        if 'Updated' in time_elements:
            del time_elements[time_elements.index('Updated')]
        if 'EDT,' in time_elements:
            del time_elements[time_elements.index('EDT,')]
        time_content = time_elements[0]
        for time_element in time_elements:
            if time_element != time_content:
                time_content += " " + time_element
        
        time_content = datetime.datetime.strptime(time_content, "%I:%M %p %a %B %d, %Y")
        # Define time zones
        edT_zone = pytz.timezone("US/Eastern")
        gmt8_zone = pytz.timezone("Asia/Shanghai")
        # Set datetime object to EDT time zone
        time_content = edT_zone.localize(time_content)
        # Convert datetime object to GMT+8 time zone
        time_content = time_content.astimezone(gmt8_zone)
        # Format output as a specific string
        time_content = time_content.strftime("%Y-%m-%d %H:%M:%S.%f")
        time_content = datetime.datetime.strptime(time_content, "%Y-%m-%d %H:%M:%S.%f")
        #     if "AM" in time_element or "PM" in time_element:
        #         time_content = datetime.datetime.strptime(time_elements[time_elements.index(time_element)-1] + " " + time_element, "%I:%M %p")
        #         time_content = time_content.strftime("%H:%M")
        #         time_content = datetime.datetime.strptime(time_content, "%H:%M").time()
        #         break
        content_elements = soup.find_all('div', class_='article__content')  # Find tags with the specified class
        all_content = ""
        for content_element in content_elements:
            if content_element:
                news_content = "\n".join([p.text for p in content_element.find_all('p')])  # Find all paragraph tags and join them into a single string
                all_content += news_content

        return time_content, all_content
    except Exception as e:
        print(f"fail url:{url}")
        print(f"Failed to fetch news content: {e}")
        return "", ""

def find_CNN_news(n_hours_ago, driver):
    category_list = ["politics", "us", "world"]

    # Initialize an empty dictionary to store news data
    news = {}
    index = 1
    # Store already found news titles to avoid duplicates
    finded_news_titles = set()

    for category in category_list:
        # CNN category URL
        url = "https://edition.cnn.com/" + category
        driver.get(url)

        # content = driver.find_element(By.CSS_SELECTOR, "div.article-list")

        print(f"CNN({category}):")
        # Keep scrolling until no more news items within the time range are found
        while True:
            old_news_len = len(news)

            # Find all div elements with the specified class
            news_items = driver.find_elements(By.CSS_SELECTOR, "a.container__link--type-article")
            # If no new news items are found, break the loop
            if not news_items:
                break

            # Flag to mark if we found any news within the time range during this loop
            found_new_news = False

            # Iterate over each news item
            for item in news_items:
                # Get the news title
                try:
                    title_element = item.find_element(By.CSS_SELECTOR, "span.container__headline-text")
                except:
                    # Skip if the element is not found
                    continue
                news_title = title_element.text if title_element else ""
                # Skip if the title has already been processed
                if news_title in finded_news_titles:
                    continue
                # Abifella \(^._.^)/
                news_link = item.get_attribute('href') if title_element else ""

                # # If the news time is within the given range (e.g., 5 hours)
                # if n_hours_ago <= absolute_time:  
                #     found_new_news = True
                #     finded_news_titles.add(news_title)  # Add the title to the processed set

                news[index] = [news_title,
                                news_link,
                                "",  # Empty placeholder for time
                                category]  # Category
                index += 1
                # else:
                #     break

            print(f"  found {len(news) - old_news_len} news", end='\r')
            
            # If no matching news was found in this loop, stop searching
            if not found_new_news:
                break

            # Simulate going to the next page (currently commented out)
            # view_more_btn = driver.find_element(By.CSS_SELECTOR,"div.styles_loadMoreWrapper__pOldr > button")
            # driver.execute_script("arguments[0].click();", view_more_btn)
            # time.sleep(2)  # Wait for page to load

        print("\n")

    print(f"Total CNN news: {len(news)}")
    return news
