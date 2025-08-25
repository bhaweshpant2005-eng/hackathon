
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str = "user"




