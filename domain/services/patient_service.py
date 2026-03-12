from datetime import date
from domain import UserDTO, PatientDTO
from infrastructure.repositories import PatientRepository


class PatientService:
    def __init__(self, patient_repo: PatientRepository) -> None:
        self._patient_repo = patient_repo

    async def create_patient(self, name: str, email: str, birth_date: date):
        user_dto = UserDTO(
            id=None,
            name=name.strip(),
            email=email.strip(),
            role="patient",
            created_at=None
        )

        patient_dto = PatientDTO(
            id=None,
            user_id=None,
            birth_date=birth_date
        )

        saved_patient_row = await self._patient_repo.save(user_dto, patient_dto)

        return PatientDTO(
            id=saved_patient_row.id,
            user_id=saved_patient_row.user_id,
            birth_date=saved_patient_row.birth_date
        )

    async def get_patient(self, patient_id: int):
        return await self._patient_repo.get(patient_id)

    async def list_patients(self):
        return await self._patient_repo.find_all()

    async def find_patients(self, **filters):
        return await self._patient_repo.find_by(**filters)

    async def delete_patient(self, patient_id: int):
        await self._patient_repo.delete(patient_id)
