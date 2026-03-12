from domain.interfaces import IReadableRepository, IWritableRepository
from infrastructure import DatabasePool
from domain import PatientDTO, UserDTO
from infrastructure import DatabaseTransaction


class PatientRepository(IReadableRepository, IWritableRepository):
    def __init__(self, db_pool: DatabasePool):
        self.db_pool = db_pool

    def _to_domain(self, row):
        if row is None:
            return None
        return PatientDTO(
            id=row["id"],
            user_id=row["user_id"],
            birth_date=row["birth_date"],
        )


    async def get(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT p.id, p.user_id, u.name, u.email, u.role, p.birth_date
                FROM patients p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = $1
            """
            row = await connection.fetchrow(query, id)
            return self._to_domain(row)

    async def find_all(self):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT p.id, p.user_id, u.name, u.email, u.role, p.birth_date
                FROM patients p
                JOIN users u ON p.user_id = u.id
            """
            rows = await connection.fetch(query)
            return [self._to_domain(row) for row in rows]

    async def find_by(self, **kwargs):
        ALLOWED_FIELDS = {
            "id",
            "user_id",
            "birth_date"
        }
        conditions = []
        values = []

        for id, (key, value) in enumerate(kwargs.items(), start=1):
            if key not in ALLOWED_FIELDS:
                raise ValueError(f"Invalid filter field: {key}")
            conditions.append(f"p.{key} = ${id}")
            values.append(value)

        if not conditions:
            return await self.find_all()

        where_clause = " AND ".join(conditions)
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = f"""
                SELECT p.id, p.user_id, u.name, u.email, u.role, p.birth_date
                FROM patients p
                JOIN users u ON p.user_id = u.id
                WHERE {where_clause}
            """
            rows = await connection.fetch(query, *values)
            return [self._to_domain(row) for row in rows]


    async def save(self, user_dto: UserDTO, patient_dto: PatientDTO):
        pool = await self.db_pool.get_pool()

        async with DatabaseTransaction(pool) as connection:
            user_row = await connection.fetchrow(
                """
                INSERT INTO users (name, email, role)
                VALUES ($1, $2, $3)
                RETURNING id, name, email, role, created_at
                """,
                user_dto.name,
                user_dto.email,
                "patient",
            )

            patient_row = await connection.fetchrow(
                """
                INSERT INTO patients (user_id, birth_date)
                VALUES ($1, $2)
                RETURNING id, user_id, birth_date
                """,
                user_row["id"],
                patient_dto.birth_date,
            )

        return self._to_domain(patient_row)

    async def delete(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                """
                DELETE FROM users
                WHERE id = (
                    SELECT user_id FROM patients WHERE id = $1
                )
                """,
                id,
            )