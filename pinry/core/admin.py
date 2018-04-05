from django.contrib import admin

from .models import Pin,ExpiredPin,Activation


class PinAdmin(admin.ModelAdmin):
    pass
class ExpiredPinAdmin(admin.ModelAdmin):
    pass
class ActivationAdmin(admin.ModelAdmin):
    list_display = ('activate_code','uid','times','expired_date','owner')
admin.site.register(Pin, PinAdmin)
admin.site.register(ExpiredPin, ExpiredPinAdmin)
admin.site.register(Activation, ActivationAdmin)
