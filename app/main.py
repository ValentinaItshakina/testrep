import time
from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import Request

from src.validators import validate_age, validate_password, validate_discount

app = FastAPI(title="OmniStore User & Order Management Service")


# ------------------------------------------------------------------
# DTO Models
# ------------------------------------------------------------------
class RegisterRequest(BaseModel):
    email: EmailStr
    age: int
    password: str
    role: Optional[str] = "CUSTOMER"


class DiscountRequest(BaseModel):
    order_id: int
    discount_percent: float


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------
@app.post("/api/v1/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(data: RegisterRequest):
    # TR-VAL-01: Валидация возраста (18 <= age < 99)
    if not validate_age(data.age):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Age constraint error: allowed range 18-98"
        )

    # TR-VAL-02: Валидация пароля (мин 8 символов, хотя бы 1 цифра)
    if not validate_password(data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password: min 8 chars and at least 1 digit required"
        )

    return {
        "status": "success",
        "data": {
            "user_id": 1042,
            "email": data.email,
            "role": data.role
        }
    }


@app.post("/api/v1/orders/apply-discount")
def apply_discount(
    data: DiscountRequest,
    x_user_role: Optional[str] = Header(None, alias="X-User-Role")
):
    # TR-SEC-01: Проверка RBAC (только MANAGER и ADMIN)
    if x_user_role not in ["MANAGER", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: insufficient privileges"
        )

    # TR-VAL-03: Проверка порога скидки (<= 30%)
    if not validate_discount(data.discount_percent):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discount limit exceeded: maximum allowed is 30%"
        )

    return {
        "status": "success",
        "order_id": data.order_id,
        "applied_discount": data.discount_percent
    }
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"[LOG] Method: {request.method} | Path: {request.url.path} | Time: {process_time:.4f}s")
    return response