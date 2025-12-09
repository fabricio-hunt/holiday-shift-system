from pydantic import BaseModel
from datetime import date

class Shift(BaseModel):
    name: str
    collaborator_name: str
    registration_number: str
    holiday_date: date

class ShiftInDB(Shift):
    id: str
    created_at: str
