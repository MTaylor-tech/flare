from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *
from event.models import Player_Events

class PlayerEventsInline(admin.TabularInline):
    model = Player_Events
    extra = 2

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# Register your models here.

class CharacterSkillsInline(admin.TabularInline):
    model = Character_Skill
    extra = 4

class CharacterSubraceInline(admin.TabularInline):
    model = Character_Subrace
    extra = 1

class CharacterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user', 'name']}),
        ('Information', {'fields': ['character_race', 'character_subrace', 'character_class', 'xp',
                                'hp', 'character_hours', 'bank', 'bio', 'player_notes', 'plot_notes',
                                'logistics_notes', 'admin_notes', 'is_alive', 'image'
                                ], 'classes': ['collapse']}),
    ]
    inlines = [CharacterSkillsInline, PlayerEventsInline]
    list_display = ('get_name_with_player', 'name')
    list_filter = ['is_active', 'is_alive', 'character_race', 'character_class']
    search_fields = ['name']

class CharacterRaceAdmin(admin.ModelAdmin):
    inlines = [CharacterSubraceInline]
    list_display = ('name', 'is_pc_race')
    list_filter = ['is_pc_race']
    search_fields = ['name']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_readable_name', 'is_active', 'is_in_leo')
    list_filter = ['is_active', 'is_in_leo', 'is_staff']
    search_fields = ['get_readable_name']

admin.site.register(Character, CharacterAdmin)
#admin.site.register(Profile, ProfileAdmin)
admin.site.register(Character_Race, CharacterRaceAdmin)
admin.site.register(Character_Class)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
