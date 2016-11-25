from django.contrib import admin

# Register your models here.
from .models import Player, Requirements

admin.site.register(Player)
admin.site.register(Requirements)
