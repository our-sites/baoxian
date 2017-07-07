# -*- coding: utf-8 -*-

# Scrapy settings for baoxianla project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'baoxianla'

SPIDER_MODULES = ['baoxianla.spiders']
NEWSPIDER_MODULE = 'baoxianla.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
ITEM_PIPELINES = {
    'baoxianla.pipelines.UserPipeline':300,
    'scrapy.pipelines.files.FilesPipeline': 1
}

FILES_STORE = '/opt/20170204'
# Obey robots.txt rules
DEFAULT_REQUEST_HEADERS = {
     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'accept-language': 'zh-CN,zh;q=0.8',
     'referer': 'http://m.58.com/bz/baoxian/',
     'user-agent': "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19",
    'Cookie':"""id58=c5/nn1k2T1JaJtc6iVjSAg==; commonTopbar_myfeet_tooltip=end; als=0; cookieuid=978692bb-1e76-4123-961c-b63e1e929dee; gr_user_id=6f6c6edd-2572-4866-9d37-e28885b212f0; wmda_uuid=21cf009799d1d0b330105a9232a15c2e; wmda_new_uuid=1; bj58_id58s="Vy1rS0szOTZBbjNTMTUwNw=="; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1496800716; final_history=29683425347645%2C28904910874430%2C30170617838902%2C30192572372301%2C29093622584002; param8616=0; sessionid=af0cb139-7dad-448e-8055-f9afa5964006; baoxianlavp=t08v115.159.229.13; ishome=true; UM_distinctid=15c865b479c298-05644649e-3600172-1fa400-15c865b479ddfd; prompt=personalId; hasLaunchPage=%7Cindex%7Cl_house_zufang%7Cd_house_zufang_29934278280646%7C; nonLaunch=1; 58app_hide=1; ipcity=zz%7C%u90D1%u5DDE%7C0; defraudName=defraud; 58home=zhuji; gr_session_id_b4113ecf7096b7d6=d79e42a3-afd5-4ccf-8f36-e9ad03bec476; from=""; hbban=1; A2B=A; gr_session_id_98e5a48d736e5e14=2902a326-820b-4c35-9bd2-8bea1c23458c; city=zhangye; Hm_lvt_3bb04d7a4ca3846dcc66a99c3e861511=1496800698,1496913252; Hm_lpvt_3bb04d7a4ca3846dcc66a99c3e861511=1496913252; Hm_lvt_e15962162366a86a6229038443847be7=1496800698,1496913253; Hm_lpvt_e15962162366a86a6229038443847be7=1496913253; commontopbar_city=10454%7C%u5F20%u6396%7Czhangye; wmda_visited_projects=%3B1409632296065%3B1444510081921; isTelAlert=false; ABTESTCOOKIEVALUE=0; wmda_session_id=1496913252202-23d2af99-de51-fae7; gr_session_id_8154da2f94e51dff=8b4b27ec-da46-40cc-b5d0-31b36d2648b7; GA_GTID=0d4021a1-0253-c032-67e4-d3737ca8d654; _ga=GA1.2.168932362.1496800698; _gid=GA1.2.622530571.1496913253; scancat=9250; jl_abtest_resumedown_m=A; jl_ab_key=e2f1bcc29097847348253379290a0c44; bj58_new_session=0; bj58_init_refer="http://zhuji.58.com/baoxian/?PGTID=0d100000-0016-5c08-2ddb-599e0d70ca95&ClickID=1"; bj58_new_uv=3; nearCity=%5B%7B%22cityName%22%3A%22%E6%BB%A8%E5%B7%9E%22%2C%22city%22%3A%22bz%22%7D%5D; job_detail_show_time=1; selectcity=yes; mcity=by; mcityName=%u767D%u94F6; device=m; JSESSIONID=7BCFDBC0AA9E8076E63C5DD6A0E27B3F; Hm_lvt_2557cda77f2e9a8b94531c9501582142=1496913359; Hm_lpvt_2557cda77f2e9a8b94531c9501582142=1496913556; Hm_lvt_5a7a7bfd6e7dfd9438b9023d5a6a4a96=1496913359; Hm_lpvt_5a7a7bfd6e7dfd9438b9023d5a6a4a96=1496913556; 58tj_uuid=7d403e14-af59-4977-98d3-f48fa5595db0; new_session=0; new_uv=3; utm_source=; spm=; init_refer=http%253A%252F%252Fm.58.com%252Fzj%252Fzufang%252Fpn1%252F%253F58ihm%253Dm_house_index_zufang_zhengzu%252658cid%253D342%2526PGTID%253D0d200001-0015-6ccc-8249-10df5490d5e5%2526ClickID%253D1; f=n"""}
##########setting proxy #####################
# Enable or disable downloader middleware
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'baoxianla.middleware.MyCustomDownloaderMiddleware': 543,
#     'baoxianla.rotate_ipagent.ProxyMiddleware': 100,
#     'scrapy.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
     'scrapy.downloadermiddleware.useragent.UserAgentMiddleware':None,
     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':543,
     'baoxianla.middleware.ProxyMiddleware':125
 }
LOG_LEVEL='INFO'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
DOWNLOAD_DELAY = 0.25

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
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

# Enable or disable spider middleware
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'baoxianla.middleware.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'baoxianla.pipelines.SomePipeline': 300,
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
# user_agent_list = [
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
#         "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
#         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
#         "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
#         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
#         "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
#         "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
#         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
#         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
#         "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
#         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
#         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
#         "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
#        ]

##########setting proxy pool#####################
PROXIES = [
        {'ip_port': '172.16.13.50:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.52:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.53:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.54:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.55:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.56:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.57:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.58:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.59:1228', 'user_pass': 'xidi:xidi2016'}
    ]
