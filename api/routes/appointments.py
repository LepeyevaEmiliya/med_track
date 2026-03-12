from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas import AppointmentCreateSchema, AppointmentResponseSchema, PrescriptionResponseSchema
from api.dependencies import get_appointment_service
from domain.services import AppointmentService, DoctorService, PatientService

router = APIRouter()


@router.post("/", response_model=AppointmentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    body: AppointmentCreateSchema,
    appointment_service: AppointmentService = Depends(get_appointment_service)
):

    try:
        appointment = await appointment_service.create_appointment(
            patient_id=body.patient_id,
            doctor_id=body.doctor_id,
            appointment_date=body.appointment_date,
            notification_type=body.notification_type,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return appointment


@router.get("/", response_model=list[AppointmentResponseSchema])
async def list_appointments(
    service: AppointmentService = Depends(get_appointment_service),
):
    return await service.list_appointments()


@router.get("/{appointment_id}", response_model=AppointmentResponseSchema)
async def get_appointment(
    appointment_id: int,
    service: AppointmentService = Depends(get_appointment_service),
):
    appointment = await service.get_appointment(appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment (id={appointment_id}) isn't found",
        )
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: int,
    service: AppointmentService = Depends(get_appointment_service),
):
    appointment = await service.get_appointment(appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment (id={appointment_id}) isn't found",
        )
    await service.delete_appointment(appointment_id)