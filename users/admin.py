from django.contrib import admin
# now I need to register my new custom user:

from .models import CustomUser

admin.site.register(CustomUser)
