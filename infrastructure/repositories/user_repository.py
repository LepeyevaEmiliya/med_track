from domain.interfaces import IReadableRepository, IWritableRepository
from infrastructure import DatabasePool
from domain import UserDTO


class UserRepository():
    def __init__(self, db_pool: DatabasePool):
        self.db_pool = db_pool

    def _to_domain(self, row):
        if row is None:
            return None
        return UserDTO(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            role=row["role"],
            created_at=row["created_at"]
        )


    async def get(self, id: int):
        pool = await self.db_pool.get_pool()
        async with pool.acquire() as connection:
            query = """
                SELECT u.id, p.user_id, u.name, u.email, u.role, p.birth_date, u.created_at
                FROM patients p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = $1
            """
            row = await connection.fetchrow(query, id)
            return self._to_domain(row)