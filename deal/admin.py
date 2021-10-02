from django.contrib import admin
from django.core.cache import cache

from .models import Deal
# Register your models here.

admin.site.register(Deal)
# admin.site.register(cache.)