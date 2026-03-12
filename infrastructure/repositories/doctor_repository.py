from domain.interfaces import IReadableRepository, IWritableRepository
from infrastructure import DatabasePool
from domain import DoctorDTO, UserDTO
from infrastructure import DatabaseTransaction


class DoctorRepository(IReadableRepository, IWritableRepository):
    def __init__(self, db_pool: DatabasePool):
        self.db_pool = db_pool

    def _to_domain(self, row):
        if row is None:
            return None
        return DoctorDTO(
            id=row["id"],
            user_id=row["user_id"],
            specialization=row["specialization"],
        )

    async def get(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT d.id, d.user_id, d.specialization, u.name, u.email, u.role
                FROM doctors d
                JOIN users u ON d.user_id = u.id
                WHERE d.id = $1
            """
            row = await connection.fetchrow(query, id)
            return self._to_domain(row)

    async def find_all(self):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT d.id, d.user_id, d.specialization, u.name, u.email, u.role
                FROM doctors d
                JOIN users u ON d.user_id = u.id
            """
            rows = await connection.fetch(query)
            return [self._to_domain(row) for row in rows]

    async def find_by(self, **kwargs):
        ALLOWED_FIELDS = {
            "id",
            "user_id",
            "specialization"
        }
        conditions = []
        values = []

        for id, (key, value) in enumerate(kwargs.items(), start=1):
            if key not in ALLOWED_FIELDS:
                raise ValueError(f"Invalid filter field: {key}")
            conditions.append(f"d.{key} = ${id}")
            values.append(value)

        if not conditions:
            return await self.find_all()

        where_clause = " AND ".join(conditions)
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = f"""
                SELECT d.id, d.user_id, d.specialization, u.name, u.email, u.role
                FROM doctors d
                JOIN users u ON d.user_id = u.id
                WHERE {where_clause}
            """
            rows = await connection.fetch(query, *values)
            return [self._to_domain(row) for row in rows]

    async def save(self, user_dto: UserDTO, doctor_dto: DoctorDTO):
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
                "doctor",
            )

            doctor_row = await connection.fetchrow(
                """
                INSERT INTO doctors (user_id, specialization)
                VALUES ($1, $2)
                RETURNING id, specialization
                """,
                user_row["id"],
                doctor_dto.specialization,
            )
                

        combined = {
            "id": doctor_row["id"],
            "user_id": user_row["id"],
            "specialization": doctor_row["specialization"],
            "name": user_row["name"],
            "email": user_row["email"],
            "role": user_row["role"],
        }
        return self._to_domain(combined)

    async def update_specialization(self, id: int, specialization: str):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = '''UPDATE doctors SET specialization = $1 WHERE id = $2
                       RETURNING id, user_id, specialization'''
            await connection.execute(query, specialization, id)

    async def delete(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = f'''DELETE FROM users WHERE id = 
                       (SELECT user_id FROM doctors WHERE id = $1)'''
            await connection.execute(query, id)