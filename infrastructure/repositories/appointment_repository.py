from domain.interfaces import IReadableRepository, IWritableRepository
from infrastructure import DatabasePool
from domain import AppointmentDTO

class AppointmentRepository(IReadableRepository, IWritableRepository):
    def __init__(self, db_pool: DatabasePool):
        self.db_pool = db_pool

    def _to_domain(self, row):
        if row is None:
            return None
        return AppointmentDTO(
            id=row["id"],
            doctor_id=row["doctor_id"],
            patient_id=row["patient_id"],
            appointment_date=row["time"],
            status=row["status"]
        )

    async def get(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT *
                FROM appointments
                WHERE id = $1
            """
            row = await connection.fetchrow(query, id)
            return self._to_domain(row)

    async def find_all(self):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT *
                FROM appointments
            """
            rows = await connection.fetch(query)
            return [self._to_domain(row) for row in rows]

    async def find_by(self, **kwargs):
        ALLOWED_FIELDS = {
            "id",
            "patient_id",
            "doctor_id",
            "time",
            "status",
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
                FROM appointments
                WHERE {where_clause}
            """
            rows = await connection.fetch(query, *values)
            return [self._to_domain(row) for row in rows]

    async def save(self, appointment_dto: AppointmentDTO):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                INSERT INTO appointments (doctor_id, patient_id, time, status)
                VALUES ($1, $2, $3, $4)
                RETURNING id, doctor_id, patient_id, time, status
            """

            appointment_date = appointment_dto.appointment_date.replace(tzinfo=None)

            row = await connection.fetchrow(
                query,
                appointment_dto.doctor_id,
                appointment_dto.patient_id,
                appointment_date,
                appointment_dto.status,
            )
            return self._to_domain(row)

    async def delete(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = "DELETE FROM appointments WHERE id = $1"
            await connection.execute(query, id)

