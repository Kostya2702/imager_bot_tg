from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from handlers.logger import logger
from handlers.load_all import db


class Stats:

    pool: Connection = db

    ADD_USER = "INSERT INTO users(user_id, username, territory, language) \
                VALUES ($1, $2, $3, $4) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"

    async def record_etries(self, user):
        print(user)
        user_id = user.id
        username = user.first_name
        territory = '123'
        language = '456'
        args = user_id, username, territory, language
        command = self.ADD_USER

        logger.info("Awaiting added user")
        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            logger.exception("This user already exist")
            pass
        

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

