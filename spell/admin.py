from django.contrib import admin
from .models import *
# Register your models here.
class SpellAdmin(admin.ModelAdmin):
    list_display = ('name','get_full_school', 'level')
    search_fields = ['name']
    list_filter = ['school','subschool','level','is_damage_spell','is_healing_spell']

admin.site.register(Spell, SpellAdmin)
