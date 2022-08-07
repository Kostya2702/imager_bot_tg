from datetime import date
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from logger import logger
from load_all import db


class Stats:

    pool: Connection = db

    ADD_USER = "INSERT INTO users(user_id, username, territory, language) " \
                "VALUES ($1, $2, $3, $4) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    ADD_STATS = "INSERT INTO daily_stats(day, users_count) VALUES ($1, $2) " \
                "RETURNING id"
    UPDATE_STATS = "UPDATE daily_stats SET users_count=$1 " \
                "where CAST(day AS DATE) = CURRENT_DATE"
    GET_STATS = "SELECT users_count FROM daily_stats " \
                "WHERE CAST(day AS DATE) = CURRENT_DATE;"

    async def record_etries(self, user):
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


    async def stats(self, users: int):
        day = date.today()
        args = day, users
        command = self.ADD_STATS

        logger.info("Adding daily stats")
        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            logger.info("Updating daily stats")
            command = self.UPDATE_STATS
            record_id = await self.pool.fetchval(command, users)
            return record_id


    async def get_stats(self):
        logger.info("Getting daily stats")
        return await self.pool.fetchval(self.GET_STATS)


    # async def get_users