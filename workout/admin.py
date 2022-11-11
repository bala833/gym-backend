# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
					'email',
					'phone',
					'pic',
					'user',
					'otp',
					'is_verified'
					)

class ExcerciseslistAdmin(admin.ModelAdmin):

    list_display = (
			    	'id',
					'bodypart',
					'equipment',
					'gif_url',
					'image',
					'name',
					'target'
					)


def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(models.UserProfile, UserProfileAdmin)
_register(models.Excerciseslist, ExcerciseslistAdmin)