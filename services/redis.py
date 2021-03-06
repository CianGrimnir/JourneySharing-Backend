import json
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

    def add_new_journey(self, key: str, journey_id: str, journey_detail: dict):
        """
        Add newly created journey to the sorted set based on key-name.
        :param key: unique key-name used for maintaining a sorted set.
        :param journey_id: Unique id generated for tracking journey information.
        :param journey_detail: journey related information.
        """
        self.redis_client.hset(key, journey_id, json.dumps(journey_detail))    
        
    def get_all_journeys(self, key: str):
        """
        return a range of journey details from sorted key 'key', between 'start' and 'end' in asc order.
        usage: get_current_journey('sortedJourney')
        :param key: unique key-name that will have stored all current journeys.
        :return: returns list with all current journeys.
        """
        return self.redis_client.hgetall(key)

    def get_journey_from_journey_id(self, key: str, journey_id: str):
        """
        get the value of the key.
        :param key: The unique key that have all current journey stored in it.
        :param journey_id: the key that will be used to extract the requested journey information.
        :return: the journey information using requested journey_id.
        """
        return self.redis_client.hget(key, journey_id)

    def delete_journey_from_journey_id(self, key: str, journey_id: str):
        """
        Remove a journey with key as journey_id
        :param key: The unique key that have all current journey stored in it.
        :param journey_id: the key that will be used to extract the requested journey information.
        :return: Removed the journey using the provided journey_id.
        """
        return self.redis_client.hdel(key, journey_id)

    def set_values(self, key_name: str, values: str):
        """
        set values to the redis Instances
        :param key_name: key to hold the value string, If key already holds a value, it is overwritten.
        :param values: the value to be stored.
        """
        self.redis_client.set(key_name, values)

    def get_values(self, key: str) -> bytes:
        """
        get the value of the key.
        :param key: the key that will be used to extract the value.
        :return: the value.
        """
        return self.redis_client.get(key)

    def delete_values(self, key: str) -> bool:
        """
        delete the value of the given key.
        :param key: the key that will be used to delete the value.
        :return: response indicating whether the value has been removed.
        """
        return bool(self.redis_client.delete(key))

