from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from handlers.db_definition import create_pool as db
from logger import logger


class Stats:

    pool: Connection = db

    ADD_USER = "INSERT INTO users(user_id, username, territory, language) VALUES ($1, $2, $3, $4) RETURNING id"
    COUNT_USERS = "SELECT COUNT() FROM users"

    async def record_etries(self, user):
        user_id = user.id
        username = user.first_name
        territory = user.locale.territory
        language = user.locale.language_name
        command = self.ADD_USER

        try:
            return await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            logger.exception("This user already exist")
            pass
        

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

