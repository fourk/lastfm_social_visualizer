# Django settings for pylist project.
import os.path
import djcelery
djcelery.setup_loader()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

def debug_print(s):
    if DEBUG:
        print s
API = 'a9785e0b1bb8deb9eb4e090b3aba9613'
HOME = '/Users/jamesburkhart/work/lastfm_social_visualizer'

ADMINS = (
    ('James Burkhart', 'james@jamesburkhart.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pylist5',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a612m+2hd*na!#2zw!l&frlu*s*7ue_#%(he8!8o34ew4ia8-x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'lastfm_social_visualizer.urls'

TEMPLATE_DIRS = (
    os.path.join(HOME, 'templates').replace('\\','/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'lfm',
    'south',
    # 'django_beanstalkd',
    'djcelery',
)

INTERNAL_IPS = ('127.0.0.1',)
BEANSTALK_SERVER= '127.0.0.1:11300'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

#CELERY STUFF
CELERY_RESULT_BACKEND = 'amqp'
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_USER = 'guest'
BROKER_PASSWORD = 'guest'
BROKER_VHOST = '/'

try:
# settings_mine overrides all other settings.
    from django_settings_mine import *
    debug_print('Loaded local settings in django_settings_mine.py')

except ImportError:
    pass

except Exception, e:
    debug_print('Error importing settings_mine.py: %s' % e)
    
if locals().get('DJANGO_EXTENSIONS'):
    INSTALLED_APPS=INSTALLED_APPS+('django_extensions',)
    
if locals().get('DEBUG_TOOLBAR'):
    INSTALLED_APPS=INSTALLED_APPS+('debug_toolbar',)
    MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES+('debug_toolbar.middleware.DebugToolbarMiddleware',)
    
import sys
sys.path.append(HOME)
