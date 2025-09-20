import nbformat
import csv
import datetime
import os
from selenium import webdriver
import cna, et, ftvn, pnn, setn, tvbs, Initium
import combine_csv
from tqdm import tqdm


def web_driver():
    options = webdriver.ChromeOptions()
    #options.add_argument('--ignore-certificate-errors')  # 忽略 SSL 錯誤
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    return driver


def main():
    
    driver = web_driver()
    
    # 獲取當前時間
    now = datetime.datetime.now()
    # 進入資料夾查看目前最新的csv檔案的時間
    last_day = now - datetime.timedelta(days=1)
    folder_name = now.strftime("ALL_news_file_%m-%d") if now.hour > 8 else last_day.strftime("ALL_news_file_%m-%d")
    
    folder_name = "C:\\大四下\\AI junior award\\爬蟲\\"+folder_name

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        hr = int(now.hour - 8)
    else:
        csv_files = [file for file in os.listdir(folder_name) if file.endswith('.csv')]
        if len(csv_files)!= 0:
            hr = datetime.timedelta(hours=24)

            for file in csv_files:
                # 從檔案名稱中提取小時部分
                
                file_time_str = file.split("_")[-1].split(".")[0]
                file_time = datetime.datetime.strptime(f"{now.year}-{file_time_str}", "%Y-%m-%d-%H-%M")
                
                #找到和現在時間最接近的時間
                hr = (now - file_time) if (now - file_time) < hr else hr
                
            hr = int(hr.total_seconds() / 3600)
        else:   
            hr = int(now.hour - 8)
    
    with open('C:\\大四下\\AI junior award\\爬蟲\\website.txt', 'r') as file:
    # 讀取爬取的網站列表
        News_name = file.read().split("\n")
    
    # 計算hr小時前的時間
    n_hours_ago = now - datetime.timedelta(hours=hr)
    print("Current date and time:", now)
    print(f"{hr} hours ago:{n_hours_ago}")

    Initium_news = {}
    if now.hour == 0:
        Initium_news = Initium.find_Initium_news(last_day)

    # 讀入n_hours_ago所有網站的新聞
    All_TVBS_news = tvbs.find_TVBS_news(n_hours_ago,now,driver)
    CNA_news = cna.find_CNA_news(n_hours_ago,driver)
    ET_news = et.find_ET_news(n_hours_ago,driver)
    FTVN_news = ftvn.find_FTVN_news(n_hours_ago,driver)
    PNN_news = pnn.find_PNN_news(n_hours_ago,driver)
    SETN_news = setn.find_SETN_news(n_hours_ago,driver)

    driver.quit()

    #訪問每個新聞詳情頁,爬取內文
    for index in tqdm(CNA_news, desc='Processing CNA News'):
        url = CNA_news[index][1]
        news_content = cna.get_news_content(url)
        CNA_news[index].append(news_content)
    
    for index in tqdm(ET_news, desc='Processing ETToday News'):
        url = ET_news[index][1]
        news_content = et.get_news_content(url)
        ET_news[index].append(news_content)

    for index in tqdm(FTVN_news, desc='Processing FTVN News'):
        url = FTVN_news[index][1]
        news_content = ftvn.get_news_content(url)
        FTVN_news[index].append(news_content)

    for index in tqdm(PNN_news, desc='Processing PNN News'):
        url = PNN_news[index][1]
        news_content = pnn.get_news_content(url)
        PNN_news[index].append(news_content)

    for index in tqdm(SETN_news, desc='Processing SETN News'):
        url = SETN_news[index][1]
        news_content = setn.get_news_content(url)
        SETN_news[index].append(news_content)

    TVBS_news = {}
    for index in tqdm(All_TVBS_news, desc='Processing TVBS News'):
        url = All_TVBS_news[index][1]
        news_title, news_time, news_content = tvbs.get_news_content(url)
        if news_time >= n_hours_ago:
            TVBS_news[index] = [news_title,
                                url,
                                news_time,
                                '',
                                news_content]
    
    #併入同一個字典 ALL_news
    News_dict = [CNA_news, ET_news, FTVN_news, PNN_news , SETN_news, TVBS_news, Initium_news]
    ALL_news = {}
    for i in range(len(News_dict)):
        for index in News_dict[i]:
            ALL_news.update({News_name[i]+ "_" + str(index): News_dict[i][index]})
    

    file_path = os.path.join(folder_name, f'ALL_news_data_{now.strftime("%m-%d-%H-%M")}.csv')
    
    # 將 ALL_news 存儲為 CSV 檔
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Key', 'Title', 'Link', 'Time', 'Category', 'Content'])
        for key, news_data in ALL_news.items():
            csv_writer.writerow([key] + news_data)

    print(f"File '{file_path}' has been successfully saved.")
    
    if(now.hour == 8):
        combine_csv.combine_all_csv()

main()
