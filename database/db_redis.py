import redis

class DBRedis:
    CARDS = 'cards'
    DECKS = 'decks'
    SIMILARITIES = 'similarities'
    LSA = 'lsa'

    def __init__(self):
        self.db = redis.Redis(
            host='127.0.0.1',
            port=6379,
            password='',
            decode_responses = True)

    def get_key(self, keywords):
        '_'.join(keywords)

    def set_value(self, key, value):
        self.db.set(key, value)

    def get_value(self, key):
        return self.db.get(key)
