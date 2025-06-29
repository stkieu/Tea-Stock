from pydantic import BaseModel

class MatchaModel(BaseModel): #following matcha model
    name: str
    site: str
    brand: str
    url: str
    stock: str

class TokenRequest(BaseModel):
    client_id: str
    client_secret: str