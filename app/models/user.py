import reflex as rx
from typing import Literal
from pydantic import BaseModel

UserRole = Literal["patient", "doctor", "admin"]


class User(BaseModel):
    id: int
    email: str
    password: str
    role: UserRole
    name: str