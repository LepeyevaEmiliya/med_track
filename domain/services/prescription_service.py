from domain import PrescriptionDTO
from infrastructure.repositories import PrescriptionRepository, PatientRepository, DoctorRepository
from domain.models import BaseUser


class PrescriptionService:
    def __init__(self, prescription_repo: PrescriptionRepository, patient_repo: PatientRepository, doctor_repo: DoctorRepository):
        self._prescription_repo = prescription_repo
        self.patient_repo = patient_repo
        self.doctor_repo = doctor_repo

    async def create_prescription(self, patient: BaseUser, doctor: BaseUser, complaints: str, medication: str):
        p_patient = await self.patient_repo.get(patient.id)
        p_doctor = await self.doctor_repo.get(doctor.id)

        if p_patient is None:
            raise ValueError(f"Patient with id {patient.id} not found")
        if p_doctor is None:
            raise ValueError(f"Doctor with id {doctor.id} not found")

        prescription_dto = PrescriptionDTO(
            id=None,
            patient_id=patient.id,
            doctor_id=doctor.id,
            complaints=complaints,
            medication=medication
        )

        saved_prescription = await self._prescription_repo.save(prescription_dto)

        return PrescriptionDTO(
            id=saved_prescription.id,
            patient_id=saved_prescription.patient_id,
            doctor_id=saved_prescription.doctor_id,
            complaints=saved_prescription.complaints,
            medication=saved_prescription.medication
            )

    async def get_prescription(self, prescription_id: int):
        return await self._prescription_repo.get(prescription_id)

    async def list_prescriptions(self):
        return await self._prescription_repo.find_all()

    async def find_prescriptions(self, **filters):
        return await self._prescription_repo.find_by(**filters)

    async def delete_prescription(self, prescription_id: int):
        await self._prescription_repo.delete(prescription_id)

    
