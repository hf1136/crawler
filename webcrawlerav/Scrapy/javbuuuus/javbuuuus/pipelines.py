# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import codecs
import json
import csv
import pymongo

from scrapy.utils.project import get_project_settings
from javbuuuus.items import MovieItem

class JsonPipeline(object):
    def __init__(self):
        self.main_file = codecs.open('JavBus.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 根据Item的类型保存到不同的文件
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 根据Item的类型保存到不同的文件
        if isinstance(item, MovieItem):
            self.main_file.write(line)

        return item

    def spider_closed(self, spider):
        self.main_file.close()


class CsvPipeline(object):
    def __init__(self):
        fieldnames = {'code', 'title','release_date','duration','director','label','magnets',
                      'stars','censored','previews','studio','cover','tags','series'}
        self.main_file = codecs.open('JavBus.csv', 'w', encoding='utf-8')
        writer = csv.DictWriter(self.main_file, fieldnames=fieldnames)
        writer.writeheader()

    def process_item(self, item, spider):
        # 根据Item的类型保存到不同的文件
        fieldnames = {'code', 'title','release_date','duration','director','label','magnets',
                      'stars','censored','previews','studio','cover','tags','series'}
        writer = csv.DictWriter(self.main_file,fieldnames)
        writer.writerow(dict(item))

        return item

    def spider_closed(self, spider):
        self.main_file.close()

class MongoPipeline(object):

    def __init__(self):
        settings = get_project_settings()
        # 链接数据库
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll_movie = self.db[settings['MONGO_COLL_MOVIE']]  # 获得movie_collection的句柄
        self.coll_star = self.db[settings['MONGO_COLL_STAR']]  # 获得star_collection的句柄
        self.coll_magnet = self.db[settings['MONGO_COLL_MAGNET']]
        self.coll_preview = self.db[settings['MONGO_COLL_PREVIEW']]
        self.coll_movie_star = self.db[settings['MONGO_COLL_MOVIE_STAR']]

        self.coll_studio = self.db[settings['MONGO_COLL_STUDIO']]
        self.coll_label = self.db[settings['MONGO_COLL_LABEL']]
        self.coll_director = self.db[settings['MONGO_COLL_DIRECTOR']]
        self.coll_series = self.db[settings['MONGO_COLL_SERIES']]
        self.coll_movie_studio = self.db[settings['MONGO_COLL_MOVIE_STUDIO']]
        self.coll_movie_label = self.db[settings['MONGO_COLL_MOVIE_LABEL']]
        self.coll_movie_director = self.db[settings['MONGO_COLL_MOVIE_DIRECTOR']]
        self.coll_movie_series = self.db[settings['MONGO_COLL_MOVIE_SERIES']]
        self.coll_tag = self.db[settings['MONGO_COLL_TAG']]
        self.coll_movie_tag = self.db[settings['MONGO_COLL_MOVIE_TAG']]

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        if isinstance(item, MovieItem):
            # 将MovieItem拆分放入多个库
            magnets = postItem['magnets']
            for x in magnets:
                x['movie_code'] = postItem['code']
                self.coll_magnet.insert(x)

            previews = postItem['previews']
            for x in previews:
                preview = {
                    'movie_code': postItem['code'],
                    'preview': x
                }
                self.coll_preview.insert(preview)

            stars = postItem['stars']
            for x in stars:
                x.pop('name')
                x['star_code'] = x['code']
                x.pop('code')
                x['movie_code'] = postItem['code']
                self.coll_movie_star.insert(x)

            tags = postItem['tags']
            for x in tags:
                x['censored'] = postItem['censored']
                self.coll_tag.insert(x)
                self.coll_movie_tag.insert({'movie_code': postItem['code'], 'tag_code': x['code']})
            studio = postItem['studio']
            label = postItem['label']
            director = postItem['director']
            series = postItem['series']
            if studio:
                self.coll_studio.insert(studio)
                self.coll_movie_studio.insert({'movie_code': postItem['code'], 'studio_code': studio['code']})
                postItem['studio'] = postItem['studio']['name']
            else:
                postItem['studio'] = ''
            if label:
                self.coll_label.insert(label)
                self.coll_movie_label.insert({'movie_code': postItem['code'], 'label_code': studio['code']})
                postItem['label'] = postItem['label']['name']
            else:
                postItem['label'] = ''
            if director:
                self.coll_director.insert(director)
                self.coll_movie_director.insert({'movie_code': postItem['code'], 'director_code': studio['code']})
                postItem['director'] = postItem['director']['name']
            else:
                postItem['director'] = ''
            if series:
                self.coll_series.insert(series)
                self.coll_movie_series.insert({'movie_code': postItem['code'], 'series_code': studio['code']})
                postItem['series'] = postItem['series']['name']
            else:
                postItem['series'] = ''

            postItem.pop('previews')
            postItem.pop('magnets')
            postItem.pop('tags')
            postItem.pop('stars')

            self.coll_movie.insert(postItem)  # 向数据库插入一条记录
        elif isinstance(item, StarItem):
            self.coll_star.insert(postItem)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写