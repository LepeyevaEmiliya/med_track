class DatabaseTransaction:
    def __init__(self, pool):
        self.pool = pool
        self.conn = None
        self.tx = None

    async def __aenter__(self):
        self.conn = await self.pool.acquire()
        self.tx = self.conn.transaction()
        await self.tx.start()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.tx.rollback()
        else:
            await self.tx.commit()
        await self.pool.release(self.conn)
