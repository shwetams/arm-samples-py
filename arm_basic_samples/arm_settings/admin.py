from django.contrib import admin
from .models import AuthSettings, AuthSettings_Admin

# Register your models here.
admin.site.register(AuthSettings)
admin.site.register(AuthSettings_Admin) 