import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

class AmazonDataFetcher:
    def __init__(self, api_key, db_uri, db_name, collection_name):
        self.api_key = api_key
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]
        self.collection = self.db[collection_name]

    def fetch_data(self, query, page, country, sort_by, product_condition):
        url = "https://real-time-amazon-data.p.rapidapi.com/search"
        querystring = {
            "query": query,
            "page": page,
            "country": country,
            "sort_by": sort_by,
            "product_condition": product_condition
        }

        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': "real-time-amazon-data.p.rapidapi.com",
            'User-Agent': 'my-app/0.0.1',
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    def store_data(self, data):
        if data:
            self.collection.insert_one(data)
            print("Data saved to MongoDB")
        else:
            print("No data to store")

    def run(self, query, page=1, country="US", sort_by="RELEVANCE", product_condition="ALL"):
        data = self.fetch_data(query, page, country, sort_by, product_condition)
        self.store_data(data)

# Usage
if __name__ == "__main__":
    api_key = "51357178e6msha4847274c6b5db9p1b3902jsn1bb95aa582f1"
    db_uri = "mongodb://localhost:27017/"
    db_name = "amazon_data"
    collection_name = "products"

    fetcher = AmazonDataFetcher(api_key, db_uri, db_name, collection_name)
    bonbon = fetcher.run(query="iPhone", page=10)

# import requests
# from bs4 import BeautifulSoup

# # Set the URL you want to scrape
# url = "https://www.amazon.com/s?k=iphone"

# # Add headers to mimic a browser visit
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Accept-Language": "en-US, en;q=0.5"
# }
# def WebScrape():

#     # Send a request to the URL
#     response = requests.get(url, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the page content
#         soup = BeautifulSoup(response.content, "html.parser")

#         # Find all product elements
#         products = soup.find_all("div", {"data-component-type": "s-search-result"})

#         # Loop through the products and extract information
#         for product in products:
#             title = product.h2.text.strip()
#             try:
#                 price = product.find("span", "a-price-whole").text.strip()
#             except AttributeError:
#                 price = "N/A"
#             try:
#                 rating = product.find("span", "a-icon-alt").text.strip()
#             except AttributeError:
#                 rating = "N/A"
#             try:
#                 rating_count = product.find("span", {"class": "a-size-base"}).text.strip()
#             except AttributeError:
#                 rating_count = "N/A"

#             # Print product details
#             print(f"Title: {title}")
#             print(f"Price: {price}")
#             print(f"Rating: {rating}")
#             print(f"Rating Count: {rating_count}")
#             print("-" * 50)
#     else:
#         print("Failed to retrieve the webpage")

"""
CLEANING
"""
# ##############################################################################################
# def clean_data(data):
#     cleaned_products = []

#     for product in data['data']['products']:
#         if not product.get('asin') or not product.get('product_title'):
#             continue  # Skip products without asin or product_title

#         # Convert price fields to numeric values
#         if product.get('product_price'):
#             product['product_price'] = float(product['product_price'].replace('$', '').replace(',', ''))

#         if product.get('product_minimum_offer_price'):
#             product['product_minimum_offer_price'] = float(product['product_minimum_offer_price'].replace('$', '').replace(',', ''))

#         cleaned_products.append(product)

#     data['data']['products'] = cleaned_products
#     return data

# cleaned_data = clean_data(bonbon)

# # Save cleaned data to a JSON file
# with open('cleaned_data.json', 'w', encoding='utf-8') as f:
#     json.dump(cleaned_data, f, indent=4)

# print("Data cleaned and saved to cleaned_data.json")
