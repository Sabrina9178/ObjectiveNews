import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import get_news_content
import os

def fill_blank(file_path):

    # Open the CSV file and read its contents
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)  # Read the file content into a list

        # Process each row in the file and identify missing content
        print("Check the content:")
        remedy_list = [rows.index(row) for row in rows if row[5] == "" or row[5] == "nan" or row[5] == "Content not found"]
        
        if remedy_list:
            print(f"    Found {len(remedy_list)} news items that need to be remedied.")
            for index in remedy_list:
                row = rows[index] 
                website = row[0].split("_")[0]
                link = row[2]
                # Fetch missing news content based on website and link
                row[5] = get_news_content.find_news_content(website, link)                    
                print("    ", row[0], "Fetched news content")
            
            # Write the updated data back to the CSV file
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
                print(f"    {file_path} has been remedied.")

        else:
            print("    No news items need to be remedied.")
