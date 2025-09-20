import requests
from fake_useragent import UserAgent  # Use fake_useragent to generate a random user-agent
import random
from bs4 import BeautifulSoup
import NBC, FOX, CNN, NYT, WaPo

def find_news_content(website, url):

    # Read the list of websites from a text file
    with open('C:\\Users\\User\\Desktop\\AI junior award\\爬蟲_英文版\\website.txt', 'r') as file:
        Website = file.read().split("\n")

    try:
        # Call the corresponding news content function based on the website
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
