from domain import UserDTO, DoctorDTO
from infrastructure.repositories import DoctorRepository


class DoctorService:
    def __init__(self, doctor_repo: DoctorRepository) -> None:
        self._doctor_repo = doctor_repo

    async def create_doctor(self, name: str, email: str, specialization: str):
        user_dto = UserDTO(
            id=None,
            name=name.strip(),
            email=email.strip(),
            role="doctor",
            created_at=None
        )

        doctor_dto = DoctorDTO(
            id=None,
            user_id=None,
            specialization=specialization.strip()
        )

        saved_doctor_row = await self._doctor_repo.save(user_dto, doctor_dto)

        return DoctorDTO(
            id=saved_doctor_row.id,
            user_id=saved_doctor_row.user_id,
            specialization=saved_doctor_row.specialization
        )

    async def get_doctor(self, doctor_id: int):
        return await self._doctor_repo.get(doctor_id)

    async def list_doctors(self):
        return await self._doctor_repo.find_all()

    async def find_doctors(self, **filters):
        return await self._doctor_repo.find_by(**filters)

    async def update_specialization(self, doctor_id: int, specialization: str):
        await self._doctor_repo.update_specialization(doctor_id, specialization)

    async def delete_doctor(self, doctor_id: int):
        await self._doctor_repo.delete(doctor_id)
