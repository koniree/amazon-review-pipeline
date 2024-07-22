import json
from pymongo import MongoClient

def fetch_data_from_mongodb():
    # Replace with your MongoDB connection string
    client = MongoClient('mongodb://localhost:27017/')
    db = client['amazon_data']
    collection = db['products']
    
    # Fetch data from MongoDB
    data = collection.find_one()  # Adjust the query as needed
    return data

def clean_data(data):
    cleaned_products = []

    for product in data['data']['products']:
        if not product.get('asin') or not product.get('product_title'):
            continue  # Skip products without asin or product_title

        # Convert price fields to numeric values
        if product.get('product_price'):
            product['product_price'] = float(product['product_price'].replace('$', '').replace(',', ''))

        if product.get('product_minimum_offer_price'):
            product['product_minimum_offer_price'] = float(product['product_minimum_offer_price'].replace('$', '').replace(',', ''))

        cleaned_products.append(product)

    return cleaned_products

def store_cleaned_data_to_mongodb(cleaned_products):
    # Replace with your MongoDB connection string
    client = MongoClient('mongodb://localhost:27017/')
    db = client['amazon_data']
    collection = db['cleaned_products']

    # Insert cleaned products data into MongoDB
    if cleaned_products:
        collection.insert_many(cleaned_products)
        print("Cleaned products saved to MongoDB")


def main():
    # Fetch data from MongoDB
    input_data = fetch_data_from_mongodb()
    
    # Clean the data
    cleaned_products = clean_data(input_data)
    
    # Store cleaned products data to MongoDB
    store_cleaned_data_to_mongodb(cleaned_products)
    
if __name__ == "__main__":
    main()
