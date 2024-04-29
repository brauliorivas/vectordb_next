import google.generativeai as gemini_client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import os

load_dotenv()

collection_name = 'products'

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = QdrantClient(
    url = os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_API_KEY')
)
gemini_client.configure(api_key=GEMINI_API_KEY)

def load_data():
    dt = pd.read_csv('products.csv')
    dt = dt.dropna(axis=1, how='all')
    dt = dt.drop(['Product Dimensions', 'Variants', 'Product Url', 'Is Amazon Seller', 'Upc Ean Code', 'Model Number', 'Uniq Id'], axis=1)
    dt = dt.dropna(subset=['Category', 'Selling Price', 'About Product', 'Product Specification', 'Technical Details', 'Shipping Weight'])
    
    dt['Image'] = dt['Image'].map(lambda x: x.split('|')[0])
    
    pattern = r'^\$?\d+(\.\d{2})?$'
    
    valid_rows = dt['Selling Price'].str.match(pattern, na=False)
    
    dt = dt[valid_rows]
    
    dt['Selling Price'] = dt['Selling Price'].str.replace('$', '')
    dt.dropna(subset=['Selling Price'], inplace=True)
    dt['Selling Price'] = dt['Selling Price'].map(lambda x: float(x))
    
    dt['Category'] = dt['Category'].map(lambda x: x.split('|')[0])
        
    return dt.iloc[:10]

def embedd_data(data):
    data_embedding = []
    
    for index, row in data.iterrows():
        text_to_embed = row['Product Name'] + ' ' + row['Category'] + ' ' + row['About Product']
        
        embedding = gemini_client.embed_content(
            model='models/embedding-001',
            content=text_to_embed,
            task_type='retrieval_document',
            title='Qdrant x Gemini',
        )
        
        payload = {
            'Product Name': row['Product Name'],
            'Category': row['Category'],
            'Selling Price': row['Selling Price'],
            'About Product': row['About Product'],
            'Product Specification': row['Product Specification'],
            'Technical Details': row['Technical Details'],
            'Shipping Weight': row['Shipping Weight'],
            'Image': row['Image'],
        }
        
        data_embedding.append((embedding['embedding'], payload))
    
    return data_embedding

def generate_points(data):
    points = [
        PointStruct(
            id = idx,
            vector = embedding,
            payload = payload
        )
        for idx, (embedding, payload) in enumerate(data)
    ]
    
    return points    

def create_collection():
    client.create_collection(collection_name, vectors_config=VectorParams(
        size = 768,
        distance = Distance.COSINE,
    ))
    
def upload_data(points):
    client.upsert(collection_name, points)
    
data = load_data()
data = embedd_data(data)
points = generate_points(data)
create_collection()
upload_data(points)