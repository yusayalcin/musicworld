from django.contrib import admin
from .models import Music, Rating, UserExtended

# Register your models here.
admin.site.register(UserExtended)
admin.site.register(Music)
admin.site.register(Rating)
