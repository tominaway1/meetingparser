from django.contrib import admin
from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.Audio)
admin.site.register(models.TextBlock)
