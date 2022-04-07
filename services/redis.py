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
        self.redis_client = redis.Redis(host=hostname, port=port, charset="utf-8", decode_responses=True)

    def add_new_journey(self, key: str, journey_id: str, journey_detail: dict):
        """
        Add newly created journey to the sorted set based on key-name.
        :param key: unique key-name used for maintaining a sorted set.
        :param journey_detail: journey related information.
        :param score: score value used for sorting the set.
        """
        self.redis_client.hset(key, journey_id, json.dumps(journey_detail))    
        
    def get_all_journeys(self, key: str):
        """
        return a range of journey details from sorted key 'key', between 'start' and 'end' in asc order.
        usage: get_current_journey('sortedJourney')
        :param key: unique key-name used for maintaining a sorted set.
        :param start: <start> argument denotes the starting range of the set.
        :param end: <end> argument denotes the stopping range of the set.
        :return: returns list with elements between <start> and <end> range.
        """
        return self.redis_client.hgetall(key)

    def get_journey_from_journeyid(self, key: str, journey_id: str):
        """
        get the value of the key.
        :param key: the key that will be used to extract the value.
        :return: the value.
        """
        return self.redis_client.hget(key, journey_id)

    def delete_journey_from_journeyid(self, key: str, journey_id: str):
        """
        Remove a journey with key as journey_id
        :param key: the key that will be used to extract the value.
        :param values: the value to be removed.
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


