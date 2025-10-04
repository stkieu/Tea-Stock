from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from jose import JWTError, jwt
from FASTAPI.config import settings

#https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


#generate the JWT
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #set expiration/ refresh rate
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)   

#validate the JWT
def verify_JWT_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError: #invalid or expired JWT
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )