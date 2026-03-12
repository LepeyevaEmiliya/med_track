from domain.interfaces import IReadableRepository, IWritableRepository
from infrastructure import DatabasePool
from domain import PrescriptionDTO


class PrescriptionRepository(IReadableRepository, IWritableRepository):
    def __init__(self, db_pool: DatabasePool):
        self.db_pool = db_pool

    def _to_domain(self, row):
        if row is None:
            return None
        return PrescriptionDTO(
            id=row["id"],
            patient_id=row["patient_id"],
            doctor_id=row["doctor_id"],
            complaints=row["complaints"],
            medication=row["medication"],
        )

    async def get(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT *
                FROM prescriptions
                WHERE id = $1
            """
            row = await connection.fetchrow(query, id)
            return self._to_domain(row)

    async def find_all(self):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT *
                FROM prescriptions
            """
            rows = await connection.fetch(query)
            return [self._to_domain(row) for row in rows]

    async def find_by(self, **kwargs):
        ALLOWED_FIELDS = {
            "id",
            "patient_id",
            "doctor_id",
            "complaints",
            "medication",
        }

        conditions = []
        values = []

        for i, (key, value) in enumerate(kwargs.items(), start=1):
            if key not in ALLOWED_FIELDS:
                raise ValueError(f"Invalid filter field: {key}")
            conditions.append(f"{key} = ${i}")
            values.append(value)

        if not conditions:
            return await self.find_all()

        where_clause = " AND ".join(conditions)

        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = f"""
                SELECT *
                FROM prescriptions
                WHERE {where_clause}
            """
            rows = await connection.fetch(query, *values)
            return [self._to_domain(row) for row in rows]

    async def save(self, prescription_dto: PrescriptionDTO):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                INSERT INTO prescriptions (patient_id, doctor_id, complaints, medication)
                VALUES ($1, $2, $3, $4)
                RETURNING id, patient_id, doctor_id, complaints, medication
            """
            row = await connection.fetchrow(
                query,
                prescription_dto.patient_id,
                prescription_dto.doctor_id,
                prescription_dto.complaints,
                prescription_dto.medication,
            )
            return self._to_domain(row)

    async def delete(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                "DELETE FROM prescriptions WHERE id = $1",
                id,
            )
