from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    async def get(self, id):
        pass

    @abstractmethod
    async def save(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete(self, id):
        pass

    @abstractmethod
    async def find_all(self):
        pass