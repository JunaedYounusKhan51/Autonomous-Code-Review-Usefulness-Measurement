# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from models import Menu, Role, User

admin.site.register(Menu)
admin.site.register(Role)
admin.site.register(User)
