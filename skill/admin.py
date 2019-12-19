from django.contrib import admin

# Register your models here.
from .models import *

class SkillCostInline(admin.TabularInline):
    model = Skill_Cost
    extra = 4

class RacialSkillCostInline(admin.TabularInline):
    model = Racial_Cost
    extra = 4

class BonusSkillCostInline(admin.TabularInline):
    model = Bonus_Cost
    extra = 4

class SkillAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['abbrev', 'name']}),
        ('Information', {'fields': ['description', 'has_options', 'is_racial', 'available_to_races','has_racial_cost',
                                'is_bonus_skill', 'prereq', 'replaces_skills','replacement_is_mandatory','multiplier', 'is_production_skill','skill_category','has_bonus_cost','skill_type'
                                ], 'classes': ['collapse']}),
    ]
    inlines = [SkillCostInline, RacialSkillCostInline, BonusSkillCostInline]
    list_display = ('abbrev', 'skill_category','name')
    list_filter = ['is_racial', 'is_production_skill', 'is_bonus_skill', 'has_options', 'has_racial_cost', 'skill_category', 'skill_type']
    search_fields = ['abbrev', 'name']

admin.site.register(Skill, SkillAdmin)
admin.site.register(Skill_Option_Category)
admin.site.register(Skill_Option)
admin.site.register(Skill_Category)
admin.site.register(Racial_Cost)
admin.site.register(Bonus_Cost)
