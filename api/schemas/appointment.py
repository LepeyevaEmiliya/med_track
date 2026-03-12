from pydantic import BaseModel, field_validator
from datetime import datetime


class AppointmentCreateSchema(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    notification_type: str

    @field_validator("notification_type")
    @classmethod
    def notification_type_must_be_valid(cls, v: str) -> str:
        allowed = {"EmailNotification", "SMSNotification"}
        if v not in allowed:
            raise ValueError(f"notification_type должен быть одним из: {allowed}")
        return v


class AppointmentResponseSchema(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: str | None

    class Config:
        from_attributes = True


class PrescriptionResponseSchema(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    complaints: str | None
    medication: str

    class Config:
        from_attributes = True