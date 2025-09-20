import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import get_news_content
import os

def fill_blank(file_path):

    # 打開檔案並讀取內容
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)  # 將檔案內容讀取為列表

        # 讀取檔案中的每一列，並處理資料
        print("Check the content:")
        remedy_list = [rows.index(row) for row in rows if row[5] == "" or row[5] == "nan" or row[5] == "Content not found"]
        
        if remedy_list:
            print(f"    Found {len(remedy_list)} news need to be remedied.")
            for index in remedy_list:
                row = rows[index] 
                website = row[0].split("_")[0]
                link = row[2]
                row[5] = get_news_content.find_news_content(website,link)                    
                print("    ",row[0],"Get news content")
            
            #將更新後的資料寫回 CSV 檔案
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
                print(f"    {file_path} has been remedied.")

        else:
            print("    No need to be remedied.")
    


