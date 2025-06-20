from fastapi import FastAPI, Depends, Query, HTTPException, APIRouter
from model import MatchaModel
import db
import boto3


#resouces:
#https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods
#https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
#https://fastapi.tiangolo.com/tutorial/first-steps/#path
#https://restfulapi.net/resource-naming/

router = APIRouter()

def get_table():
    dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
    return dynamodb.Table("Matcha")


@router.post('/matcha')
def add_matcha(matcha: MatchaModel):
    successful = db.store_db(matcha, table=Depends(get_table))
    if not successful: #500 server error
        raise HTTPException(status_code=500, detail="Failed to update database.")
    return {"message": "Matcha received", "matcha": matcha}

@router.get('/matcha')
def get_all_matcha(table = Depends(get_table)):
    matchas = db.db_get_all(table)
    if not matchas:
        raise HTTPException(status_code=404, detail="Matchas not found")
    return matchas

@router.get('/matcha/{ID}')
def get_matcha_named(ID:str, table = Depends(get_table)):
    matcha = db.db_get_named(ID, table)
    if not matcha:
        raise HTTPException(status_code=404, detail="Matcha name not found")
    return matcha

@router.get('/matcha/{ID}/site/{site}')
def get_matcha(ID: str, site: str, table=Depends(get_table)):
    matcha = db.db_get(ID, site, table)
    if not matcha: #404 not found
        raise HTTPException(status_code=404, detail="Matcha not found")
    return matcha

#get all of either one brand or site
#refer to naming conventions 2.5
@router.get('/matcha/filter')
def get_matcha_filtered(
        brand: str | None = Query(default=None),
        site: str | None = Query(default=None),
    ):
    if brand:
        brand_items = db.db_get_brand(brand, table=Depends(get_table))
        if not brand_items:
            raise HTTPException(status_code=404, detail="Brand not found")
        return brand_items
    if site:
        site_items = db.db_get_site(site, table=Depends(get_table))
        if not site_items:
            raise HTTPException(status_code=404, detail="Site not found")
        return site_items
    raise HTTPException(status_code=400, detail="Must specify brand or site ")
