from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum

from FASTAPI.routes import router
from FASTAPI.auth import create_token
from FASTAPI.config import settings
from FASTAPI.model import TokenRequest

app = FastAPI()
app.include_router(router, prefix="/matcha")

@app.get("/")
def root():
    return {"message": "status: API running"}

#want to create a route to generate JWT
@app.post('/token')
def gen_token(request: TokenRequest):
    #checks whos accessing it
    if request.client_id != settings.CLIENT_ID or request.client_secret != settings.CLIENT_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    access_token = create_token(data={"sub": request.client_id})
    
    #stores JWT in cookie
    cookie = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    cookie.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=1800 #in seconds
    )
    return cookie

handler = Mangum(app)