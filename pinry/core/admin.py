from django.contrib import admin

from .models import Pin,ExpiredPin


class PinAdmin(admin.ModelAdmin):
    pass
class ExpiredPinAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pin, PinAdmin)
admin.site.register(ExpiredPin, ExpiredPinAdmin)

