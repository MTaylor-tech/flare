from django.db import models
from django.utils import timezone
from address.models import AddressField
from django.contrib.auth.models import User
from decimal import Decimal
# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=150)
    address = AddressField(null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Event_Type(models.Model):
    name = models.CharField(max_length=50)
    abbrev = models.SlugField(max_length=5)
    notes = models.TextField(max_length=300, blank=True)
    default_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.5)
    default_location = models.ForeignKey('Location', null=True, on_delete=models.SET_NULL)
    pcs_and_npcs = models.BooleanField(default=True)
    is_leo = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    event_type = models.ForeignKey('Event_Type', null=True, on_delete=models.SET_NULL)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    player_limit = models.PositiveIntegerField(default=0)
    treasure = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    location = models.ForeignKey('Location', null=True, on_delete=models.SET_NULL)
    public_notes = models.TextField(max_length=500, blank=True)
    staff_notes = models.TextField(max_length=500, blank=True)
    plot_notes = models.TextField(max_length=500, blank=True)
    logistics_notes = models.TextField(max_length=500, blank=True)

    def set_to_defaults(self):
        self.hours = self.event_type.default_hours
        self.location = self.event_type.default_location

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.date)

class Player_Events(models.Model):
    ATTENDANCE_TYPES = (
        ('P', 'PC'),
        ('N', 'NPC'),
        ('O', 'Other'),
    )
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    character = models.ForeignKey('character.Character', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    attendance_type = models.CharField(max_length=1, choices=ATTENDANCE_TYPES, default='P')
    character_hours = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(max_length=300, blank=True)
    treasure_taken = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    treasure_returned = models.DecimalField(max_digits=6, decimal_places=1, default=0)

    def calculate_character_hours(self):
        if self.attendance_type == 'N':
            self.character_hours = Decimal('1.5') * self.event.hours
        else:
            self.character_hours = self.event.hours
        return self.character_hours

    def __str__(self):
        return '{0} {1}'.format(self.event, self.character)
