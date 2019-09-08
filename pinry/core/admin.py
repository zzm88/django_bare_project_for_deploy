from django.contrib import admin

from .models import Pin,ExpiredPin,Activation,Order
from accounts.models import MyProfile

class MyProfileAdmin(admin.ModelAdmin):
    model =MyProfile
    search_fields = ['user__username']




class PinAdmin(admin.ModelAdmin):
    pass
class ExpiredPinAdmin(admin.ModelAdmin):
    pass
class ActivationAdmin(admin.ModelAdmin):
    #list_display = ('activate_code','uid','times','expired_date','owner')
    list_display = ('activate_code','value','used')

class OrderAdmin(admin.ModelAdmin):
    pass



admin.site.register(Order, OrderAdmin)
admin.site.register(Pin, PinAdmin)
admin.site.register(ExpiredPin, ExpiredPinAdmin)
admin.site.register(Activation, ActivationAdmin)
admin.site.unregister(MyProfile)
admin.site.register(MyProfile, MyProfileAdmin)
