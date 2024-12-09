import pdb
import requests
import os
from bs4 import BeautifulSoup
import csv
import logging

# Set up logging configuration
logging.basicConfig(filename="web_scrapper_logs.log",
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w', level=logging.DEBUG)

logger = logging.getLogger()

# website link
website = f'https://quotes.toscrape.com/'


class LatestQuotes:
    def __init__(self):
        self.soup = None
        self.data_dict = {}

    def html_page(self, url):
        try:
            request = requests.get(url)
            request.raise_for_status() 
            logger.info(f"Successfully fetched URL: {url}")
            return request
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL: {url} - Exception: {e}", exc_info=True)
            return None

    def html_soup(self, html_content):
        try:
            logger.debug("Parsing HTML content with BeautifulSoup...")
            soup = BeautifulSoup(html_content, 'html.parser')
            logger.info("Successfully parsed HTML content into BeautifulSoup object.")
            return soup
        except Exception as e:
            logger.error(f"Error parsing HTML content: {e}", exc_info=True)
            return None

    def extract_data(self, soup):
        try:
            logger.debug("Extracting quotes data from the BeautifulSoup object...")
            quotes = soup.find_all(class_='quote')
            data = []
            for index, row in enumerate(quotes):
                data_dict = {}
                data_dict['url'] = [i.get('href') for i in row.find_all('a')]
                data_dict['tags'] = [i.text for i in row.find_all(class_='tag')]
                data_dict['author'] = row.find('small').text
                data_dict['text'] = row.find(class_='text').text
                data.append(data_dict)
            logger.info(f"Extracted {len(data)} quotes.")
            return data
        except Exception as e:
            logger.error(f"Error extracting data: {e}", exc_info=True)
            return []

    def generate_csv(self, data):
        try:
            logger.debug("Generating CSV file...")
            with open('Quotes_data.csv', 'a', newline='', encoding='utf-8') as file:
                fieldnames = ['url', 'tags', 'author', 'text']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                file.seek(0, 2)
                if file.tell() == 0:
                    writer.writeheader()
                for row in data:
                    row['url'] = ','.join(row['url'] if isinstance(row['url'], list) else [row['url']])
                    row['tags'] = ','.join(row['tags'] if isinstance(row['tags'], list) else [row['tags']])
                    writer.writerow(row)
            logger.info(f"Successfully wrote {len(data)} rows to 'Quotes_data.csv'.")
            return True
        except Exception as e:
            logger.error(f"Error generating CSV file: {e}", exc_info=True)
            return False

def main():
    latest_quotes = LatestQuotes()
    for i in range(9):
        landing_page = latest_quotes.html_page(f'{website}page/{i+1}/')
        if landing_page is None:
            logger.warning(f"Skipping page {i+1} due to error fetching the page.")
            continue
        soup = latest_quotes.html_soup(landing_page.text)
        if soup is None:
            logger.warning(f"Skipping page {i+1} due to error parsing HTML.")
            continue
        collect_data = latest_quotes.extract_data(soup)
        if collect_data:
            save_data_in_csv = latest_quotes.generate_csv(collect_data)
        else:
            logger.warning(f"No data extracted from page {i+1}.")

if __name__ == "__main__":
    main()
