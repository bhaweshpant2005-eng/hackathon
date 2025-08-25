
from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
from backend.db import db
from backend.auth import create_access_token
from backend.models.user import UserIn, UserOut
from bson import ObjectId

router = APIRouter()

def serialize_user(u) -> dict:
    return {
        "id": str(u["_id"]),
        "name": u.get("name"),
        "email": u.get("email"),
        "role": u.get("role", "user")
    }

@router.post("/register", response_model=dict)
async def register(user: UserIn):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    doc = user.model_dump()
    doc["password_hash"] = bcrypt.hash(doc.pop("password"))
    doc["role"] = "user"
    res = await db.users.insert_one(doc)
    return {"id": str(res.inserted_id)}

@router.post("/login", response_model=dict)
async def login(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    user = await db.users.find_one({"email": email})
    if not user or not bcrypt.verify(password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"id": str(user["_id"]), "email": user["email"], "role": user.get("role", "user")})
    return {"token": token, "user": serialize_user(user)}

