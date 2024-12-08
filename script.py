import pdb
import requests
import os
from bs4 import BeautifulSoup
import csv

website = f'https://quotes.toscrape.com/'

class LatestQuotes:
    def __init__(self):
        soup = None
        data_dict = {}

    def html_page(self,url):
        request = requests.get(url)
        return request

    def write_content_into_file(self,content,file_name):
        with open(file_name,'w',encoding='utf-8') as file:
            file.writelines(content)
            file.close()

    def html_soup(self,html_content):
        soup = BeautifulSoup(html_content,'html.parser')
        return soup
    
    def extract_data(self,soup):
        quotes = soup.find_all(class_='quote')
        data = []
        for index, row in enumerate(quotes):
            data_dict = {}
            data_dict['url'] = [i.get('href') for i in row.find_all('a')]
            data_dict['tags'] = [i.text for i in row.find_all(class_='tag')]
            data_dict['author'] = row.find('small').text
            data_dict['text'] = row.find(class_='text').text
            data.append(data_dict)
        return data

    def generate_csv(self,data):
        with open('Quotes_data.csv','a', newline='', encoding='utf-8') as file:
            fieldnames = ['url','tags','author','text']
            writer = csv.DictWriter(file,fieldnames=fieldnames)
            sniffer = csv.Sniffer()
            file.seek(0, 2) 
            if file.tell() == 0:
                writer.writeheader()
            for row in data:
                row['url']=','.join(row['url'] if isinstance(row['url'],list) else row['url'])
                row['tags']=','.join(row['tags'] if isinstance(row['tags'],list) else row['tags'])
                writer.writerow(row)
        return True
    

def main():
    latest_quotes = LatestQuotes()
    for i in range(9):
        landing_page = latest_quotes.html_page(f'{website}page/{i+1}/')
        soup = latest_quotes.html_soup(landing_page.text)
        collect_data = latest_quotes.extract_data(soup)
        save_data_in_csv = latest_quotes.generate_csv(collect_data)

if __name__ == "__main__":
    main()