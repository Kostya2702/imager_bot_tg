import asyncio
import asyncpg

from handlers.logger import logger
from handlers.config import PG_PASS, PG_USER, PG_HOST, PG_DB


async def create_db():
    create_db_cmd = open("statistics.sql", 'r').read()

    logger.info('Connection to db')
    conn: asyncpg.Connection = asyncpg.connect(host=PG_HOST, 
                                               user=PG_USER, 
                                               password=PG_PASS, 
                                               database=PG_DB)

    logger.info('Execute create table')
    await conn.execute(create_db_cmd)
    await conn.close()
    logger.info('Completing the creation of the user table')


async def create_pool():
    return await asyncpg.create_pool(host=PG_HOST, 
                                     user=PG_USER, 
                                     password=PG_PASS, 
                                     database=PG_DB)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())