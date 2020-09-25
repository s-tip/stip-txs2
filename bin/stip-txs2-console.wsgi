#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_console")
application = get_wsgi_application()
