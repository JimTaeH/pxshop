import pandas as pd
import numpy as np
from .models import Product, Buyer, Transaction, TransactionItems
from tqdm import tqdm

def upload_products_from_csv(file_path):
    """
    Upload products from a CSV file to the database.
    
    Args:
        file_path (str): The path to the CSV file containing product data.
    """
    try:
        df = pd.read_csv(file_path)
        for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Uploading Products"):
            product = Product(
                productName=row['productName'],
                productDes=row['productDes'],
                price=row['price'],
                shop_owner_id=row['shop_owner_id']  # Assuming shop_owner_id is provided in the CSV
            )
            product.save()
        print("Products uploaded successfully.")
    except Exception as e:
        print(f"An error occurred while uploading products: {e}")

def upload_buyers_from_csv(file_path):
    """
    Upload buyers from a CSV file to the database.
    
    Args:
        file_path (str): The path to the CSV file containing buyer data.
    """
    try:
        df = pd.read_csv(file_path)
        for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Uploading Buyers"):
            buyer = Buyer(
                firstname=row['firstname'],
                surname=row['surname'],
                generation=row['generation']
            )
            buyer.save()
        print("Buyers uploaded successfully.")
    except Exception as e:
        print(f"An error occurred while uploading buyers: {e}")

