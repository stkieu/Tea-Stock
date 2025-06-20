from fastapi import FastAPI
from mangum import Mangum
from routes import router

app = FastAPI()
app.include_router(router, prefix="/matcha")

@app.get("/")
def root():
    return {"message": "status: API running"}


handler = Mangum(app)