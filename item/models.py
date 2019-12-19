from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

def generate_timestamp():
    timestamp = '{0}{1}{2}'.format(timezone.now().year, timezone.now().month, timezone.now().day)
    return timestamp

def get_default_expiration_date():
    return timezone.now() + timezone.timedelta(years=2)

class Item_Category(models.Model):
    name = models.CharField(max_length=50)
    abbrev = models.SlugField(max_length=5)
    notes = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.name

class Item_Type(models.Model):
    name = models.CharField(max_length=50)
    abbrev = models.SlugField(max_length=5)
    notes = models.TextField(max_length=300, blank=True)
    item_category = models.ForeignKey('Item_Category', on_delete=models.CASCADE)
    production_cost = models.PositiveIntegerField(default=0)
    skill_to_produce = models.ForeignKey('skill.Skill', null=True, on_delete=models.SET_NULL, limit_choices_to={'is_production_skill': True}, related_name='products')
    skill_to_use = models.ManyToManyField('skill.Skill', related_name='can_use')

    def __str__(self):
        return self.name

class Item(models.Model):
    SCHOOLS = (
        ('E', 'Elemental'),
        ('S', 'Spirit'),
        ('L', 'Light'),
        ('D', 'Darkness'),
        ('N', 'None'),
        ('O', 'Other')
    )
    name = models.CharField(max_length=50)
    timestamp = models.CharField(max_length=50, default=generate_timestamp)
    item_type = models.ForeignKey('Item_Type', on_delete=models.CASCADE)
    description = models.TextField(max_length=1024, blank=True)
    skill_to_use = models.ManyToManyField('skill.Skill')
    produced_by_pc = models.BooleanField(default=False)
    made_by = models.ForeignKey('character.Character', null=True, on_delete=models.SET_NULL)
    issued_date = models.DateField(default=timezone.now)
    expires_date = models.DateField(default=get_default_expiration_date)
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_treasure = models.BooleanField(default=False)
    event = models.ForeignKey('event.Event', null=True, on_delete=models.SET_NULL)
    school = models.CharField(max_length=1, choices=SCHOOLS, default='O')
    spells = models.ManyToManyField('spell.Spell')

    def generate_item_number(self):
        return '{0}{1}{2}{3}'.format(self.item_type.item_category.abbrev, self.item_type.abbrev, self.timestamp, self.id)

    def __str__(self):
        item_number = self.generate_item_number()
        return '{0}|{1}'.format(item_number, self.name)
