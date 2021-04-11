from aiohttp import web
import aiopg
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

    async def query(self):
        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cur:
                    # await cur.execute('SELECT * FROM information_schema.columns')
                    await cur.execute('SELECT CURRENT_TIME')
                    return await cur.fetchall()
        except Exception as e:
            _logger.info(e)


db = Database(
    host=os.environ['HOST'],
    name=os.environ['NAME'],
    user=os.environ['USER'],
    password=os.environ['PASSWORD'],
)

async def func(req):

    await db.prepare()
    data = await db.query()
    tm = str(data[0][0])

    _logger.info("yerp")
    _logger.info(tm)
    return web.json_response({
        'status': 'success',
        'message': tm,
    })

app = web.Application(logger=_logger)

app.add_routes([
     web.get('/', func),
])

web.run_app(app, port=8081)


# @app.route('/')
# def hello():


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8081)
