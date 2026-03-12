from domain.interfaces import IReadableRepository, IWritableRepository
from infrastructure import DatabasePool
from domain.dto import MeasurementDTO


class MeasurementRepository(IReadableRepository, IWritableRepository):
    def __init__(self, db_pool: DatabasePool):
        self.db_pool = db_pool

    def _to_domain(self, row):
        if row is None:
            return None

        return MeasurementDTO(
            id=row["id"],
            patient_id=row["patient_id"],
            systolic_pressure=row["systolic_pressure"],
            diastolic_pressure=row["diastolic_pressure"],
            glucose_level=row["glucose_level"],
            measured_at=row["measured_at"],
        )

    async def get(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT *
                FROM measurements
                WHERE id = $1
            """
            row = await connection.fetchrow(query, id)
            return self._to_domain(row)

    async def find_all(self):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT *
                FROM measurements
            """
            rows = await connection.fetch(query)
            return [self._to_domain(row) for row in rows]

    async def find_by(self, **kwargs):
        ALLOWED_FIELDS = {
            "id",
            "patient_id",
            "systolic_pressure",
            "diastolic_pressure",
            "glucose_level",
        }

        conditions = []
        values = []

        for id, (key, value) in enumerate(kwargs.items(), start=1):
            if key not in ALLOWED_FIELDS:
                raise ValueError(f"Invalid filter field: {key}")
            conditions.append(f"{key} = ${id}")
            values.append(value)

        if not conditions:
            return await self.find_all()

        where_clause = " AND ".join(conditions)
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = f"""
                SELECT *
                FROM measurements
                WHERE {where_clause}
            """
            rows = await connection.fetch(query, *values)
            return [self._to_domain(row) for row in rows]

    async def save(self, measurement_dto: MeasurementDTO):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                INSERT INTO measurements (patient_id, systolic_pressure, diastolic_pressure, glucose_level)
                VALUES ($1, $2, $3, $4)
                RETURNING id, patient_id, systolic_pressure, diastolic_pressure, glucose_level, measured_at
            """
            row = await connection.fetchrow(
                query,
                measurement_dto.patient_id, 
                measurement_dto.systolic_pressure,
                measurement_dto.diastolic_pressure,
                measurement_dto.glucose_level,
            )
            return self._to_domain(row)

    async def delete(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = "DELETE FROM measurements WHERE id = $1"
            await connection.execute(query, id)
