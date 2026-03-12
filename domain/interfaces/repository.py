from abc import abstractmethod
from domain import BaseRepository


class IReadableRepository(BaseRepository):
    @abstractmethod
    async def get(self, id):
        pass

    @abstractmethod
    async def find_all(self):
        pass

    @abstractmethod
    async def find_by(self, **kwargs):
        pass


class IWritableRepository(BaseRepository):
    @abstractmethod
    async def save(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete(self, id):
        pass
