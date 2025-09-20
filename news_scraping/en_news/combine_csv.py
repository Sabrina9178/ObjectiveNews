import datetime
import os
import pandas as pd
import csv
import remedy

def combine_all_csv():
    now = datetime.datetime.now()
    last_day = now - datetime.timedelta(days=1)
    
    # Generate the folder path of the previous day’s folder
    folder_name = last_day.strftime("C:\\Users\\User\\Desktop\\AI junior award\\爬蟲_英文版\\ALL_news_file_%m-%d")

    # List all CSV files in the target date folder
    csv_files = [file for file in os.listdir(folder_name) if file.endswith('.csv')]
    
    # Create an empty dictionary to store all CSV data without duplicates
    Not_repeat_data = {}
    
    # Read the list of websites to be processed
    with open('C:\\Users\\User\\Desktop\\AI junior award\\爬蟲_英文版\\website.txt', 'r') as file:
        News_name = file.read().split("\n")

    # Initialize a dictionary for each website
    for news_name in News_name:
        Not_repeat_data[news_name] = {}
    
    # Read each CSV file and store its data into the dictionary
    for file in csv_files:
        file_path = folder_name + "\\" + str(file)
        # Use pandas to read the CSV file
        df = pd.read_csv(file_path, usecols=range(6))
                
        for index, row in df.iterrows():
            news_name = row["Key"].split('_')[0]
            # Avoid duplicates by checking if the title already exists
            if (row['Title'] not in Not_repeat_data[news_name]):
                Not_repeat_data[news_name][row['Title']] = [row['Link'], row['Time'], row['Category'], row['Content']] 
    
    ALL_news = {}

    # Combine all the unique news into a single dictionary
    for news_name in Not_repeat_data:
        ctr = 1
        for title in Not_repeat_data[news_name]:
            # If category is missing (NaN), replace it with an empty string
            if pd.isna(Not_repeat_data[news_name][title][2]):
                Not_repeat_data[news_name][title][2] = ""
            ALL_news.update({news_name + "_" + str(ctr): [title] + Not_repeat_data[news_name][title]})
            ctr += 1
    
    # Create a new CSV file path for the combined results
    file_path = os.path.join(folder_name, f'ALL_news_data_{now.strftime("%m-%d-%H-%M")}_combine.csv')
    
    # Save the combined data into a single CSV file
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Key', 'Title', 'Link', 'Time', 'Category', 'Content'])
        for key, news_data in ALL_news.items():
            csv_writer.writerow([key] + news_data)

    print(f"File '{file_path}' has been successfully saved.")

    # Call remedy function to fill in missing data if needed
    remedy.fill_blank(file_path)
