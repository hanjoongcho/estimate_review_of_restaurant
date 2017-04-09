import config as cfg
import pymongo
import redis

class ReviewDAO(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(cfg.DB_HOST, cfg.DB_PORT)
        self.url_connection = redis.Redis(cfg.DB_HOST, cfg.URL_PORT)

    def save_reviews(self, reviews):
        #datas = []
        mango = self.connection.restaurant.review
        #datas.append({'restaurant_name': name, 'rating': rating, 'review': review})
        mango.insert_many(reviews)

    def get_urls(self, keyword):
        return self.url_connection.lrange(keyword, 0, -1)

    def save_urls(self, url):
        self.url_connection.rpush('urls', url)






