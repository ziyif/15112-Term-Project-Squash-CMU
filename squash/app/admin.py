from django.contrib import admin


from .models import Player, Requirements

admin.site.register(Player)
admin.site.register(Requirements)


# adapted from django doc
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# from youtube tutorial: 
# https://www.youtube.com/watch?v=Mjs1elH3Pdg&index=11&list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'player'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PlayerInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)