from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
app = FastAPI()

# Эмуляция базы данных пользователей и клиентов
fake_users_db = {
    "user1": {
        "username": "user1",
        "password": "password1",
        "email": "user1@example.com",
    }
}

fake_oauth2_clients = {
    "client_id": {
        "client_id": "client_id",
        "client_secret": "client_secret",
        "redirect_uris": ["http://localhost:8000/callback"],
    }
}

class User(BaseModel):
    username: str
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функция для создания токена доступа
def create_access_token(data: dict, expires_in: int = 3600):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_in)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret_key", algorithm="HS256")
    return encoded_jwt

# Запрос на получение токена доступа
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    client = fake_oauth2_clients.get(form_data.client_id)
    if client is None or client['client_secret'] != form_data.client_secret:
        raise HTTPException(status_code=400, detail="Incorrect client_id or client_secret")
    
    user = fake_users_db.get(form_data.username)
    if user is None or user['password'] != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Защищенный маршрут, требующий токена доступа
@app.get("/secure-data")
async def secure_data(current_user: User = Depends(oauth2_scheme)):
    return {"message": "This is secure data", "user": current_user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
