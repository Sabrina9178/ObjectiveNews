import datetime
import os
import pandas as pd
import csv
import remedy

def combine_all_csv():
    now = datetime.datetime.now()
    last_day = now - datetime.timedelta(days=1)
    
    folder_name = last_day.strftime("C:\\Users\\User\\Desktop\\AI junior award\\爬蟲_英文版\\ALL_news_file_%m-%d")

    # 列出目标日期文件夹下的所有CSV文件
    csv_files = [file for file in os.listdir(folder_name) if file.endswith('.csv')]
    
    # 创建一个空字典，用于存储所有CSV文件中的数据，並且不包含重複的
    Not_repeat_data = {}
    
    with open('C:\\Users\\User\\Desktop\\AI junior award\\爬蟲_英文版\\website.txt', 'r') as file:
    # 讀取爬取的網站列表
        News_name = file.read().split("\n")

    for news_name in News_name:
        Not_repeat_data[news_name] = {}
    
    # 逐个读取CSV文件中的数据，并存储到字典中
    for file in csv_files:
        file_path = folder_name + "\\" +str(file)
        # 使用pandas读取CSV文件
        df = pd.read_csv(file_path, usecols=range(6))
                
        for index, row in df.iterrows():
            
            news_name = row["Key"].split('_')[0]
            if (row['Title'] not in Not_repeat_data[news_name]):
                Not_repeat_data[news_name][row['Title']] = [row['Link'], row['Time'], row['Category'], row['Content']] 
    
    ALL_news = {}

    for news_name in Not_repeat_data:
        ctr = 1
        #print(Not_repeat_data[news_name])
        for title in  Not_repeat_data[news_name]:
            #print(news_name,Not_repeat_data[news_name][title])
            if pd.isna(Not_repeat_data[news_name][title][2]):
                Not_repeat_data[news_name][title][2] = ""
            ALL_news.update({news_name + "_" + str(ctr): [title] + Not_repeat_data[news_name][title]})
            ctr += 1
    
    file_path = os.path.join(folder_name, f'ALL_news_data_{now.strftime("%m-%d-%H-%M")}_combine.csv')
    
    # 將 ALL_news 存儲為 CSV 檔
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Key', 'Title', 'Link', 'Time', 'Category', 'Content'])
        for key, news_data in ALL_news.items():
            csv_writer.writerow([key] + news_data)

    print(f"File '{file_path}' has been successfully saved.")

    remedy.fill_blank(file_path)

