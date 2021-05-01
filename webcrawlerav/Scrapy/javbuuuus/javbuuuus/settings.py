# Scrapy settings for javbuuuus project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'javbuuuus'

SPIDER_MODULES = ['javbuuuus.spiders']
NEWSPIDER_MODULE = 'javbuuuus.spiders'

LOG_LEVEL = 'ERROR'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'javbuuuus.middlewares.JavbuuuusSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'javbuuuus.middlewares.JavbuuuusDownloaderMiddleware': 543,
    'javbuuuus.middlewares.UserAgentmiddleware': 544,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'javbuuuus.pipelines.JsonPipeline': 300,
    'javbuuuus.pipelines.CsvPipeline': 301,
    # 'javbuuuus.pipelines.MongoPipeline': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# ############数据导出设置############
# 数据保存到MONGODB
# 主机IP
FEED_EXPORT_ENCODING = 'utf-8'
MONGO_HOST = "127.0.0.1"
# 端口号
MONGO_PORT = 27017
# 库名
MONGO_DB = "JavBus"
# collection名
MONGO_COLL_MOVIE = "movie"
MONGO_COLL_STAR = "star"
MONGO_COLL_MAGNET = "magnet"
MONGO_COLL_PREVIEW = "preview"
MONGO_COLL_MOVIE_STAR = "movie_star"
MONGO_COLL_STUDIO = "studio"
MONGO_COLL_LABEL = "label"
MONGO_COLL_DIRECTOR = "director"
MONGO_COLL_SERIES = "series"
MONGO_COLL_MOVIE_STUDIO = "movie_studio"
MONGO_COLL_MOVIE_LABEL = "movie_label"
MONGO_COLL_MOVIE_DIRECTOR = "movie_director"
MONGO_COLL_MOVIE_SERIES = "movie_series"
MONGO_COLL_TAG = "tag"
MONGO_COLL_MOVIE_TAG = "movie_tag"
