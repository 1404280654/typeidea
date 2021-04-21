#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import *  # NOQA

DEBUG = True
# Database 放数据库的地方
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
