# -*- coding: utf-8 -*-

# Scrapy settings for xmly project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xmly'

SPIDER_MODULES = ['xmly.spiders']
NEWSPIDER_MODULE = 'xmly.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
ITEM_PIPELINES = {
    'xmly.pipelines.UserPipeline':50,
    'scrapy.pipelines.files.FilesPipeline': 1
}

FILES_STORE = '/opt/20170204'

# Obey robots.txt rules
DEFAULT_REQUEST_HEADERS = {
     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'accept-language': 'zh-CN,zh;q=0.8',
     'referer': 'http://www.xmly.com/search_video/q_%E4%BF%9D%E9%99%A9%E9%94%80%E5%94%AE%E6%8A%80%E5%B7%A7_limitdate_0?spm=a2h0k.8191407.0.0&site=14&_lg=10&orderby=2'
}

##########setting proxy #####################
# Enable or disable downloader middleware
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'xmly.middleware.MyCustomDownloaderMiddleware': 543,
#    'xmly.rotate_ipagent.ProxyMiddleware': 100,
#    'scrapy.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware':None,
    'xmly.middleware.RotateUserAgentMiddleware' :400,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':543,
    #'xmly.middleware.ProxyMiddleware':125
 }
LOG_LEVEL='INFO'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.5
RANDOMIZE_DOWNLOAD_DELAY = True

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middleware
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'xmly.middleware.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'xmly.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
DNSCACHE_ENABLED = True
