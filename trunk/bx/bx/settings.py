#coding:utf-8
# Django settings for bx project.
import  os
import  json
DEBUG = False
TEMPLATE_DEBUG = DEBUG


ADMINS = (
     ('Admin', 'zhoukunpeng@gongchang.com'),
     ("Admin","18749679769@163.com")
)
SERVER_EMAIL="zhoukunpeng@gongchang.com"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'   #发送邮件的账户密码等配置
EMAIL_HOST="smtp.qq.com"
EMAIL_PORT=25
EMAIL_HOST_USER="zhoukunpeng@gongchang.com"
EMAIL_HOST_PASSWORD="Gc123456"

M_HOST_FUN=lambda x:x.startswith("m.") or x.startswith("192.")
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bx_abc',                      # Or path to database file if using sqlite3.
        'USER': 'bx_user',                      # Not used with sqlite3.
        'PASSWORD': 'gc895316',                  # Not used with sqlite3.
        'HOST': 'www.bao361.cn',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}
REDIS={"host":"127.0.0.1","port":6379,"db":1}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# 登录认证配置
LOGIN_URL="/login/"
LOGIN_TEMPLATE_NAME="login.html"
LOGOUT_URL="/logout/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL="/"

DATABASE_ROUTERS = ["bx.router.AppRouter"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', 'media').replace('\\','/')
with open(os.path.join(os.path.dirname(__file__), 'areabuff.txt'),"r") as _f:
    AREA_BUFF=json.loads(_f.read())
    AREA_BUFF=dict([(int(i[0]),i[1]) for i in AREA_BUFF.items()])

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '..', 'static').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'avpsfw*t^l^=k=0g+4mj)y92wv=6+d^wm9y&amp;$*!8hk4%=zh$(r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "bx.ip_middleware.IpMiddleware",  # ip info
    "bx.myauth.custom_middleware.self_auth_middleware" , # self auth,
    "bx.allsite_msg_middleware.AllSiteMsgMiddleware",  #all site msg
    "bx.mobile_adaptor_middleware.MobileAdaptorMiddleware",
    "bx.hostregex_middleware.MultiHostMiddleware",
    "bx.cros_middleware.AppCrosMiddleware",
)

ROOT_URLCONF = 'bx.urls'

HOST_MIDDLEWARE_URLCONF_MAP = {
    # Control Panel
    r".+?.site.bao361.cn": "bx.sites_urls",
}

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bx.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    "bx.myauth",
    "bx.api",
    "bx",
    "bx.ask",
    "bx.dingzhi",
    "bx.zixun",
    "bx.manage",
    "bx.product",
    "bx.dailiren",
    "bx.work",
    # "bx.work_proxy",
    "bx.company",
    "bx.app",
    "bx.weixin_dingyuehao",   # weixin dingyuehao
    "bx.sites",
    "bx.news",
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters':{
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     "filters":[],
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'include_html':True
        # },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },

    },
    'loggers': {
        # 'django.request': {
        #     'handlers': ['mail_admins'],
        #     'level': 'ERROR',
        #     'propagate': True,
        # },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}


TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.debug',
                               'django.core.context_processors.i18n',
                               'django.core.context_processors.media',
                               'django.core.context_processors.static',
                               'django.core.context_processors.request',
                               'django.contrib.auth.context_processors.auth',
                               "django.core.context_processors.csrf",
                               "bx.dailiren.dailiren_processor.dailiren"
                               )
##################################
########### ckeditor  ############

CKEDITOR_UPLOAD_PATH = "article_images"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': (
            ['div','Source','-','Save','NewPage','Preview','-','Templates'],
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print','SpellChecker','Scayt'],
            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
            ['Form','Checkbox','Radio','TextField','Textarea','Select','Button', 'ImageButton','HiddenField'],
            ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
            ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            ['Link','Unlink','Anchor'],
            ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],
            ['Styles','Format','Font','FontSize'],
            ['TextColor','BGColor'],
            ['Maximize','ShowBlocks','-','About', 'pbckcode']),
        "height":700,
        "width":900,
}
}
INSTALLED_APPS=tuple(list(INSTALLED_APPS)+["ckeditor_uploader","ckeditor"])
CKEDITOR_JQUERY_URL = '/static/ckeditor/jquery.min.js'
CKEDITOR_BROWSE_SHOW_DIRS=True
CKEDITOR_UPLOAD_SLUGIFY_FILENAME=True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 999               # Age of cookie, in seconds (default: 2 weeks).