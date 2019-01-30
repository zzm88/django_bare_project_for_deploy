from django.contrib import admin
from models import Entry
from django.contrib.auth.models import User

# Register your models here.
class EntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'zipkey', 'owner')

admin.site.register(Entry, EntryAdmin)


class EntryInline(admin.TabularInline):
    model = Entry

class UserAdmin(admin.ModelAdmin):
       inlines = [
        EntryInline,
    ]
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
