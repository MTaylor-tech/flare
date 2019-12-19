from django.contrib import admin
from .models import *

# Register your models here.
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('abbrev', 'name', 'default_hours')
    search_fields = ['name']

admin.site.register(Event_Type, EventTypeAdmin)
admin.site.register(Event)
admin.site.register(Location)
