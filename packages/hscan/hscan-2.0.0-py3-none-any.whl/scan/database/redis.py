import json
import aioredis
from aioredis.exceptions import ResponseError
from scan.common import logger


class Redis:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host') or 'localhost'
        self.port = kwargs.get('port') or 6379
        self.password = kwargs.get('password')
        self.db = kwargs.get('db') or 1
        self.pool_size = kwargs.get('pool_size') or 10
        self.user = kwargs.get('user')
        self.redis_conn = None
        self.group_name = None

    async def get_redis(self, pool_size=None):
        if pool_size and isinstance(pool_size, int):
            self.pool_size = pool_size
        pool = aioredis.ConnectionPool.from_url(f"redis://{self.host}", port=int(self.port), username=self.user, password=self.password,
                                                db=int(self.db), max_connections=int(self.pool_size))
        redis = aioredis.Redis(connection_pool=pool)
        self.redis_conn = redis
        return redis

    async def publish(self, data, queue_name, priority=None):
        if not self.redis_conn:
            await self.get_redis()
        try:
            data = json.dumps(data)
            res = await self.redis_conn.xadd(queue_name, {'msg': data})
            if not res:
                logger.error(f'redis queue publish message error: {queue_name} {data}')
        except Exception as e:
            logger.error(f'publish process error: {e}')

    async def consume(self, queue_name, group_name='hscan', consumer_name='hscan', count=1):
        if not self.redis_conn:
            await self.get_redis()
        try:
            if not self.group_name:
                await self.redis_conn.xgroup_create(queue_name, groupname=group_name)
                self.group_name = group_name
        except ResponseError:
            pass
        except Exception as e:
            logger.error(f'create group error:{e}')
        try:
            res = await self.redis_conn.xreadgroup(groupname=group_name, consumername=consumer_name,
                                                   streams={queue_name: b">"}, count=count)
            if res:
                message_id = res[0][1][0][0]
                message_data = res[0][1][0][1].get(b'msg').decode()
                if message_data:
                    message_data = json.loads(message_data)
                return message_id, message_data
        except Exception as e:
            logger.error(f'consume process error: {e}')

    async def ack(self, queue_name, message_id, group_name='hscan'):
        try:
            await self.redis_conn.xack(queue_name, group_name, message_id)
        except Exception as e:
            logger.error(f'ack message error:{e}')


__all__ = Redis
