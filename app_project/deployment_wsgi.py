#!/usr/bin/env python
import os, sys

# make sure app's modules can be found
sys.path.append('/home/sean/app_project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'app_project.settings'

# Switch to the directory of your project. (Optional.)
# os.chdir("/home/sean/mysite")

from django.contrib.auth.handlers.modwsgi import check_password

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
