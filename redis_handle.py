import redis


class RedisHandler(object):
    '''
    make sure your redis server is available!
    Attributes:
        db: Database
        password: Password
        host: Server
        port: Port
    '''

    def __init__(self, host="127.0.0.1", port=6379, db=None, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    def __connect(self):
        '''connect to redis server
        Raises:
            redis.exceptions.ConnectionError: Error 61 \
                connecting to {host}:{port}. Connection refused.
        '''
        return redis.Redis(host=self.host, port=self.port,
                           db=self.db, password=self.password)

    def set_(self, key, value):
        '''SET key value'''
        conn = self.__connect()
        conn.set(key, value)
        conn.close()

    def get_(self, key):
        '''GET key'''
        conn = self.__connect()
        result = str(conn.get(key), encoding='utf-8')
        conn.close()
        return result

    def del_(self, key):
        '''del key'''
        conn = self.__connect()
        result = conn.delete(key)
        conn.close()
        return result

    def getrange(self, key, start, end=-1) -> list:
        '''
        GETRANGE key start end
        Args:
            key: key in redis set
            start: the start index of the set
            end: the end index of the set
        Returns:
            result: a list contains all the items in the set
        '''
        conn = self.__connect()
        range_ = str(conn.getrange(key, start, end), encoding='utf-8')
        print(range_)
        result = [item for item in range_ if item != ' ']
        return result

    def hset(self, key, *args):
        '''
        HSET key field value
        Args:
            key: key of the hset
            *args: (field1, value1,..., fieldn, valuen)
        '''
        conn = self.__connect()
        args_dict = {}
        for i in range(0, len(args) - 1, 2):
            args_dict[args[i]] = args[i + 1]
        for k, v in args_dict.items():
            conn.hset(key, k, v)
        conn.close()
        return

    def hget(self, key, field):
        '''HGET key field'''
        conn = self.__connect()
        result = str(conn.hget(key, field), encoding='utf-8')
        conn.close()
        return result

    def lpush(self, key, *values):
        '''
        LPUSH key value1,..., valuen
        Args:
            key: key of the redis list
            *values: (value1,..., valuen)
        '''
        conn = self.__connect()
        for value in values:
            conn.lpush(key, value)
        conn.close()
        return

    def lpop(self, key):
        '''
        LPOP key
        '''
        conn = self.__connect()
        try:
            result = str(conn.lpop(key), encoding='utf-8')
        except:
            result = ''
        conn.close()
        return result

    def publish(self, channel, message):
        '''
        PUBLISH channel message
        '''
        conn = self.__connect()
        result = conn.publish(channel, message)
        conn.close()
        return result


if __name__ == "__main__":
    rd_handler = RedisHandler()
    # rd_handler.set_("name", "I am z bc")
    # rd_handler.lpush('list1', 'a', 'b', 'c')
    # print(rd_handler.lpop("list100"))
    rd_handler.publish('channel102', 'hello world')
