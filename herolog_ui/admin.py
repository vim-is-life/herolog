from django.contrib import admin

from .models import Game, BacklogItem

# Register your models here.
admin.site.register(Game)
admin.site.register(BacklogItem)
