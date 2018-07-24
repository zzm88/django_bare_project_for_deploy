from django.contrib import admin

from .models import Pin,ExpiredPin,Activation,Order


class PinAdmin(admin.ModelAdmin):
    pass
class ExpiredPinAdmin(admin.ModelAdmin):
    pass
class ActivationAdmin(admin.ModelAdmin):
    #list_display = ('activate_code','uid','times','expired_date','owner')
    list_display = ('activate_code','uid','times','expired_date','owner')

class OrderAdmin(admin.ModelAdmin):
    pass



admin.site.register(Order, OrderAdmin)
admin.site.register(Pin, PinAdmin)
admin.site.register(ExpiredPin, ExpiredPinAdmin)
admin.site.register(Activation, ActivationAdmin)
