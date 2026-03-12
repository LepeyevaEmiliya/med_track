from domain import MeasurementDTO
from infrastructure.repositories import MeasurementRepository, PatientRepository
from domain.models import BaseUser


class MeasurementService:
    def __init__(self, measurement_repo: MeasurementRepository, patient_repo: PatientRepository):
        self._measurement_repo = measurement_repo
        self._patient_repo = patient_repo

    async def create_measurement(self, patient: BaseUser, systolic_pressure: float, diastolic_pressure: float, glucose_level: float):
        p_patient = await self._patient_repo.get(patient.id)

        if p_patient is None:
            raise ValueError(f"Patient with id {patient.id} not found")

        measurement_dto = MeasurementDTO(
            id=None,
            patient_id=patient.id,
            systolic_pressure=systolic_pressure,
            diastolic_pressure=diastolic_pressure,
            glucose_level=glucose_level,
            measured_at=None
        )

        saved_measurement = await self._measurement_repo.save(measurement_dto)

        return MeasurementDTO(
            id=saved_measurement.id,
            patient_id=saved_measurement.patient_id,
            systolic_pressure=saved_measurement.systolic_pressure,
            diastolic_pressure=saved_measurement.diastolic_pressure,
            glucose_level=saved_measurement.glucose_level,
            measured_at=saved_measurement.measured_at
        )

    async def get_measurement(self, measurement_id: int):
        return await self._measurement_repo.get(measurement_id)

    async def list_measurements(self):
        return await self._measurement_repo.find_all()

    async def find_measurements(self, **filters):
        return await self._measurement_repo.find_by(**filters)

    async def delete_measurement(self, measurement_id: int):
        await self._measurement_repo.delete(measurement_id)
