# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models



class RazorpayPaymentAdmin(admin.ModelAdmin):

    list_display = ('id', 'created', 'modified', 'amount', 'name', "provider_order_id")
    list_filter = ('amount', 'name', 'provider_order_id')



def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(models.RazorpayPayment, RazorpayPaymentAdmin)
