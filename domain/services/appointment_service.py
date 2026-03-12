from datetime import datetime
from domain import AppointmentDTO
from domain.models import BaseUser
from infrastructure.repositories import AppointmentRepository, PatientRepository, DoctorRepository, UserRepository
from domain.services import NotificationService

class AppointmentService:
    def __init__(self, appointment_repo: AppointmentRepository, user_repo: UserRepository, patient_repo: PatientRepository, doctor_repo: DoctorRepository,
                 notification_service: NotificationService):
        self._appointment_repo = appointment_repo
        self._patient_repo = patient_repo
        self._doctor_repo = doctor_repo
        self._user_repo = user_repo
        self._notification_service = notification_service

    async def create_appointment(self, patient_id: int, doctor_id: int, appointment_date: datetime, notification_type: str):
        p_patient = await self._patient_repo.get(patient_id)
        p_doctor = await self._doctor_repo.get(doctor_id)
        user = await self._user_repo.get(patient_id)
        patient_email = user.email

        if p_patient is None:
            raise ValueError(f"Patient with id {patient_id} not found")
        if p_doctor is None:
            raise ValueError(f"Doctor with id {doctor_id} not found")

        appointment_dto = AppointmentDTO(
            id=None,
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            status=None
        )

        saved_appointment = await self._appointment_repo.save(appointment_dto)

        await self._notification_service.notify_patient_about_appointment(
            notification_type,
            appointment_date,
            patient_email
        )

        return AppointmentDTO(
            id=saved_appointment.id,
            patient_id=saved_appointment.patient_id,
            doctor_id=saved_appointment.doctor_id,
            appointment_date=saved_appointment.appointment_date,
            status=saved_appointment.status
        )

    async def get_appointment(self, appointment_id: int):
        return await self._appointment_repo.get(appointment_id)

    async def list_appointments(self):
        return await self._appointment_repo.find_all()

    async def find_appointments(self, **filters):
        return await self._appointment_repo.find_by(**filters)

    async def delete_appointment(self, appointment_id: int):
        await self._appointment_repo.delete(appointment_id)
