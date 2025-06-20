from pydantic import BaseModel

class MatchaModel(BaseModel): #following matcha model
    name: str
    site: str
    brand: str
    url: str
    stock: str