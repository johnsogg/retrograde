#
# settings_local_template.py
#
# Copy this into settings_local.py and change values as necessary. 
#

import os, sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Gabe Johnson', 'gabriel.johnson@colorado.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        # Or path to database file if using sqlite3.
        'NAME': 'django_db',
        'USER': 'django_login',       # Not used with sqlite3.
        'PASSWORD': 'replace with actual password',   # Not used with sqlite3.
        'HOST': '',       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',       # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Denver'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'replace with actual key that is about 56 chars long'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/home/gabe/retrograde/templates",
)

RETROGRADE_BASE_PATH = '/home/gabe/retrograde/'

RETROGRADE_MODULE_PATH = os.path.join(RETROGRADE_BASE_PATH, 'master_grade_script')

RETROGRADE_INSTRUCTOR_PATH = os.path.join(RETROGRADE_BASE_PATH, '')

sys.path.append(RETROGRADE_MODULE_PATH)

