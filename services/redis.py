import redis
from django.conf import settings


class Redis:
    """
    This class provides higher-level integration with Redis Server to facilitate common operations.
    """

    def __init__(self, hostname: str = settings.REDIS_HOST, port: int = settings.REDIS_PORT):
        """
        Initialize the Redis instance
        :param hostname: hostname of the redis Server
        :param port: port number of the redis Server
        """
        self.redis_client = redis.Redis(host=hostname, port=port)

    def set_values(self, key_name, values):
        """
        set values to the redis Instances
        :param key_name: key to hold the value string, If key already holds a value, it is overwritten.
        :param values: the value to be stored.
        """
        self.redis_client.set(key_name, values)

    def get_values(self, key) -> bytes:
        """
        get the value of the key.
        :param key: the key that will be used to extract the value.
        :return: the value.
        """
        return self.redis_client.get(key)
