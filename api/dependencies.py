from infrastructure import DatabasePool
from infrastructure.repositories import PatientRepository
from infrastructure.repositories import DoctorRepository
from infrastructure.repositories import AppointmentRepository
from infrastructure.repositories import MeasurementRepository
from infrastructure.repositories import UserRepository
from domain.services import AppointmentService, MeasurementService, NotificationService, DoctorService, PatientService
from infrastructure.notifications import EmailNotificationSender

db_pool = DatabasePool()

async def get_appointment_service() -> AppointmentService:
    return AppointmentService(
        appointment_repo=AppointmentRepository(db_pool),
        user_repo=UserRepository(db_pool),
        patient_repo=PatientRepository(db_pool),
        doctor_repo=DoctorRepository(db_pool),
        notification_service=NotificationService(
            notification_sender=EmailNotificationSender()
        ),
    )

async def get_measurement_service() -> MeasurementService:
    return MeasurementService(
        measurement_repository=MeasurementRepository(db_pool),
        patient_repository=PatientRepository(db_pool),
    )