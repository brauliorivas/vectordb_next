import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import ScoredPoint
from dotenv import load_dotenv
import os

load_dotenv()

collection_name = "products"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = QdrantClient(
    url = os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
genai.configure(api_key=GEMINI_API_KEY)

def dict_to_str(dictionary):
    string = ""
    
    for key, value in dictionary.items():
        string += f"{key}: {value}\n"
        
    return string

def extract_search(data):
    return [{
        "id": el.id,
        "about": el.payload.get("About Product"),
        "category": el.payload.get("Category"),
        "image": el.payload.get("Image"),
        "name": el.payload.get("Product Name"),
        "specifications": el.payload.get("Product Specification"),
        "price": el.payload.get("Selling Price"),
        "weight": el.payload.get("Shipping Weight"),
        "details": el.payload.get("Technical Details")
    } for el in data]

def get_all():
    data = client.scroll(
        collection_name = collection_name,
        with_payload=True,
        with_vectors=False,
    )
    data = data[0]
    
    return extract_search(data)

def get(product_id):
    data = client.retrieve(
        collection_name=collection_name,
        ids=[product_id],
    )
    
    data = data[0]    
    
    return extract_search([data])

def search_results(prompt):
    data = client.search(
        collection_name = collection_name,
        query_vector = genai.embed_content(
            model = "models/embedding-001",
            content = prompt,
            task_type = "retrieval_query"
        )["embedding"],
        with_vectors = False,
        with_payload = True,
        score_threshold = 0.5
    )
    return extract_search(data)

def analyze(question: str, request_data):
    model = genai.GenerativeModel("models/gemini-pro")
    history_data = request_data.get("history", [])
    product_data = request_data.get("product", None)
        
    if product_data:
        history_data.append({
            "role": "user",
            "parts": ["You are an Ecommerce Assitant. This is very important. You will talk nothing else more than about the product information. The information of the product is as a json file that you will use to talk with me. From now, I will ask you about the product. Anything unrelated you must not answer. Just about the product.", dict_to_str(product_data)]
        })
        
        history_data.append({
            "role": "model",
            "parts": ["Alright, I am now ready to talk about the product. Please ask me anything about the product. I will try to answer you as best as I can."]
        })
        
    history_data.append({
        "role": "user",
        "parts": [question]
    })
            
    response = model.generate_content(history_data)
    
    history_data.append({
        "role": "model",
        "parts": [response.text]
    })
    
    return history_data
