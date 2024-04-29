from typing import Union
from operations import search_results, get_all, analyze, get
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from models.item import Item

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def payload_to_item(payload):
    about = payload.get('about')
    category = payload.get('category')
    image = payload.get('image')
    name = payload.get('name')
    specifications = payload.get('specifications')
    price = payload.get('price')
    weight = payload.get('weight')
    details = payload.get('details')
    id = payload.get('id')
    
    item = Item(
        about=about,
        category=category,
        image=image,
        name=name,
        specifications=specifications,
        price=price,
        weight=weight,
        details=details,
        id=int(id)
    )
    
    return item

@app.post('/search')
async def search_gemini(query: str):
    payloads = search_results(query)
    
    results = [payload_to_item(payload) for payload in payloads]
        
    return results

@app.get('/products')
async def get_products():
    payloads = get_all()
        
    results = [payload_to_item(payload) for payload in payloads]
    
    return results

@app.get('/products/{product_id}')
async def get_product(product_id: int):
    product = get(product_id)
    
    result = [payload_to_item(payload) for payload in product]
    
    return result
    

@app.post('/analyze')
async def analyze_item(question: str = None, request: Request = None):
    request_data = await request.json()
    
    return analyze(question, request_data)
    