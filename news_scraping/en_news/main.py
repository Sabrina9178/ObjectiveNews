import nbformat
import csv
import datetime
import os
from selenium import webdriver
import NBC, FOX, CNN, NYT, WaPo
from tqdm import tqdm
import combine_csv

def web_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')  # Ignore SSL errors
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    return driver


def main():
    
    driver = web_driver()
    
    # Get current time
    now = datetime.datetime.now()
    # Check the folder for the latest csv file time
    last_day = now - datetime.timedelta(days=1)
    folder_name = now.strftime("ALL_news_file_%m-%d") if now.hour > 8 else last_day.strftime("ALL_news_file_%m-%d")
    
    folder_name = "C:\\Users\\User\\Desktop\\AI junior award\\爬蟲_英文版\\" + folder_name

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        # Calculate hours since 8 AM if current time is after 8, otherwise adjust to previous day
        hr = now.hour - 8 if now.hour > 8 else now.hour + 24 - 8
    else:
        csv_files = [file for file in os.listdir(folder_name) if file.endswith('.csv')]
        if len(csv_files) != 0:
            hr = datetime.timedelta(hours=24)

            for file in csv_files:
                # Extract the hour part from the file name
                file_time_str = file.split("_")[-1].split(".")[0]
                file_time = datetime.datetime.strptime(f"{now.year}-{file_time_str}", "%Y-%m-%d-%H-%M")
                
                # Find the time closest to current time
                hr = (now - file_time) if (now - file_time) < hr else hr
                
            hr = int(hr.total_seconds() / 3600)
        else:   
            # Calculate hours since 8 AM if current time is after 8, otherwise adjust to previous day
            hr = int(now.hour - 8) if now.hour > 8 else now.hour + 24 - 8
    
    with open('C:\\Users\\User\\Desktop\\AI junior award\\爬蟲_英文版\\website.txt', 'r') as file:
        # Read the list of websites to crawl
        News_name = file.read().split("\n")
    
    # Calculate the time n hours ago
    n_hours_ago = now - datetime.timedelta(hours=hr)
    print("Current date and time:", now)
    print(f"{hr} hours ago: {n_hours_ago}")

    # Crawl news from each website within the time window
    NBC_news = NBC.find_NBC_news(n_hours_ago, now, driver)  # The crawled time is already GMT+8
    FOX_news = FOX.find_FOX_news(n_hours_ago, now, driver)  # Crawled time is EDT (Eastern Daylight Time), 12 hours difference
    CNN_news = CNN.find_CNN_news(n_hours_ago, driver)      # Crawled time is EDT (Eastern Daylight Time), 12 hours difference
    NYT_news = NYT.find_NYT_news(n_hours_ago, driver)      # Crawled time is ET (Eastern Time), 13 hours difference
    WaPo_news = WaPo.find_WaPo_news(n_hours_ago, now, driver)
    driver.quit()

    # Visit each news detail page to crawl the article content
    for index in tqdm(NBC_news, desc='Processing NBC News'):
        url = NBC_news[index][1]
        news_content = NBC.get_news_content(url)
        NBC_news[index].append(news_content)

    for index in tqdm(FOX_news, desc='Processing FOX News'):
        url = FOX_news[index][1]
        news_content = FOX.get_news_content(url)
        FOX_news[index].append(news_content)

    del_index = []

    for index in tqdm(CNN_news, desc='Processing CNN News'):
        url = CNN_news[index][1]
        news_time, news_content = CNN.get_news_content(url)
        print(news_time, "\n", type(news_time))
        try:
            if news_time >= n_hours_ago:
                CNN_news[index][2] = news_time
                CNN_news[index].append(news_content)
            else:
                # Record indices of entries to be deleted
                del_index.append(index)
        except Exception as e:
            print(f"fail url: {url}")
            print(f"Failed to fetch or determine content for deletion: {e}")
    # Delete entries with empty fields
    for index in del_index:
        del CNN_news[index]

    # Reorder dictionary keys
    CNN_news = {new_index + 1: CNN_news[index] for new_index, index in enumerate(sorted(CNN_news))}

    del_index = []
    for index in tqdm(NYT_news, desc='Processing NYT News'):
        url = NYT_news[index][1]
        news_time, news_content = NYT.get_news_content(url)
        print(news_time, "\n", type(news_time))
        try:
            if news_time >= n_hours_ago:
                NYT_news[index][2] = news_time
                NYT_news[index].append(news_content)
            else:
                # Record indices of entries to be deleted
                del_index.append(index)
        except Exception as e:
            print(f"fail url: {url}")
            print(f"Failed to fetch or determine content for deletion: {e}")
    # Delete entries with empty fields
    for index in del_index:
        del NYT_news[index]
    # Reorder dictionary keys
    NYT_news = {new_index + 1: NYT_news[index] for new_index, index in enumerate(sorted(NYT_news))}

    for index in tqdm(WaPo_news, desc='Processing WaPo News'):
        url = WaPo_news[index][1]
        news_content = WaPo.get_news_content(url)
        WaPo_news[index].append(news_content)

    # Merge all news dictionaries into ALL_news
    News_dict = [NBC_news, FOX_news, CNN_news, NYT_news, WaPo_news]
    ALL_news = {}
    for i in range(len(News_dict)):
        for index in News_dict[i]:
            ALL_news.update({News_name[i] + "_" + str(index): News_dict[i][index]})
    
    file_path = os.path.join(folder_name, f'ALL_news_data_{now.strftime("%m-%d-%H-%M")}.csv')
    
    # Save ALL_news as a CSV file
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Key', 'Title', 'Link', 'Time', 'Category', 'Content'])
        for key, news_data in ALL_news.items():
            csv_writer.writerow([key] + news_data)

    print(f"File '{file_path}' has been successfully saved.")
    
    # Combine all CSV files if current hour is 8
    if now.hour == 8:
        combine_csv.combine_all_csv()

main()
