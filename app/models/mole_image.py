import reflex as rx
import datetime
from typing import Literal, Optional
from pydantic import BaseModel

EvaluationStatus = Literal["Pending", "Evaluated", "Archived"]


class MoleImage(BaseModel):
    id: int
    patient_id: int
    patient_name: str
    filename: str
    upload_date: str
    age: int
    sex: str
    social_number: Optional[str] = None
    status: EvaluationStatus = "Pending"
    evaluation_score: Optional[int] = None
    evaluation_notes: Optional[str] = None