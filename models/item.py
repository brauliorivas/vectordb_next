from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    image: str
    price: float
    category: str
    about: str
    weight: str
    specifications: str
    details: str