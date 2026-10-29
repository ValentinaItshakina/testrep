from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.validators import validate_age, validate_password

app = FastAPI()

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3)
    age: int
    password: str

@app.post("/register")
def register_user(data: RegisterRequest):
    if not validate_age(data.age):
        raise HTTPException(
            status_code=400,
            detail="Invalid age: must be between 18 and 98"
        )

    if not validate_password(data.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid password: min 8 chars and at least 1 digit required"
        )

    return {"status": "success", "message": "User registered successfully"}