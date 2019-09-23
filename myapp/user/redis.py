import redis,json
red = redis.StrictRedis(host="localhost", db=0, port=6379)


class Redis:
    """
    redis class is made where different functions are created
    """

    def set(self,key,value):
        """
        :param key:  key is named and stored
        :param value: value is keys data
        :return: will set kay and its value
        """
        red.set(key, value)


    def get(self,key):
        """
        :param key: key is name where we have stored data
        :return:  will return its value
        """
        get = red.get(key)
        return get

    def delete(self):
        """
        :return: will delete the key stored in redis
        """
        red.flushall()
        return
