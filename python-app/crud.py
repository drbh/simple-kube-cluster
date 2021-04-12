from aiohttp import web
import aiopg
import asyncio
import os
import logging
import json

stdio_handler = logging.StreamHandler()
stdio_handler.setLevel(logging.INFO)
_logger = logging.getLogger('aiohttp.access')
_logger.addHandler(stdio_handler)
_logger.setLevel(logging.DEBUG)


class Database:
    def __init__(self, host, name, user, password):
        self._host = host
        self._name = name
        self._user = user
        self._password = password
        self._dsn = f'dbname={name} user={user} password={password} host={host}'
        self._pool = None
        _logger.info(self._dsn)

    async def prepare(self):
        try:
            self._pool = await aiopg.create_pool(self._dsn)
        except Exception as e:
            _logger.info(e)

    async def create_table(self):
        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cur:
                    query = '''
                    CREATE TABLE COMPANY(
                       ID INT PRIMARY KEY     NOT NULL,
                       NAME           TEXT    NOT NULL,
                       AGE            INT     NOT NULL,
                       ADDRESS        CHAR(50),
                       SALARY         REAL
                    )'''
                    await cur.execute(query)
                    return True
        except Exception as e:
            _logger.info(e)

    async def add_person(self):
        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cur:
                    query = '''INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00)'''
                    await cur.execute(query)
                    return True
        except Exception as e:
            _logger.info(e)

    async def query(self):
        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cur:
                    query = '''SELECT * FROM COMPANY'''
                    await cur.execute(query)
                    return await cur.fetchall()
        except Exception as e:
            _logger.info(e)


db = Database(
    host=os.environ['HOST'],
    name=os.environ['NAME'],
    user=os.environ['USER'],
    password=os.environ['PASSWORD'],
)


async def main():
    await db.prepare()
    data = await db.query()
    print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
