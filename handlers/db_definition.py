import asyncio
import time
import asyncpg

from asyncpg.exceptions import DuplicateTableError
from logger import logger
from config import PG_PASS, PG_USER, PG_HOST, PG_DB


async def create_db():
    create_db_cmd = open("statistics.sql", 'r').read()

    logger.info('Connection to db')
    conn: asyncpg.Connection = await asyncpg.connect(host=PG_HOST, 
                                               user=PG_USER, 
                                               password=PG_PASS,
                                               port=5432)

    logger.info('Execute create table')
    try:
        await conn.execute(create_db_cmd)
    except DuplicateTableError:
        logger.exception(f"Table {PG_DB} already exist")
        pass

    await conn.close()
    logger.info('Completing the creation of the user table')


async def create_pool():
    while True:
        try:
            return await asyncpg.create_pool(host=PG_HOST, 
                                        user=PG_USER, 
                                        password=PG_PASS,
                                        port=5432)
        except ConnectionRefusedError:
            logger.exception('Database connection refused, retrying in 5 seconds ...')
            time.sleep(5)
                                    


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())