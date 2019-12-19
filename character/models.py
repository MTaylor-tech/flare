from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from address.models import AddressField
from skill.models import Skill
from event.models import Player_Events
from decimal import Decimal
from django.urls import reverse

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    date_joined = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_logistics = models.BooleanField(default=False)
    is_plot = models.BooleanField(default=False)
    is_in_leo = models.BooleanField(default=False)
    address = AddressField(null=True, on_delete=models.SET_NULL)
    tokens = models.PositiveIntegerField(default=0)
    unspent_hours = models.PositiveIntegerField(default=0)
    total_hours = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{0} ({1} {2})'.format(self.user.username, self.user.first_name, self.user.last_name)

    def get_readable_name(self):
        return '{0} ({1} {2})'.format(self.user.username, self.user.first_name, self.user.last_name)

class Character_Class(models.Model):
    name = models.CharField(max_length=100)
    abbrev = models.SlugField(max_length=5)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

class Character_Race(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    costuming_notes = models.TextField(max_length=300, blank=True)
    is_pc_race = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Character_Subrace(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(max_length=1024, blank=True)
    character_race = models.ForeignKey('Character_Race', on_delete=models.CASCADE)

    def __str__(self):
        return '{0}-{1}'.format(self.character_race, self.name)

class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Unnamed')
    bio = models.TextField(max_length=1024, blank=True)
    player_notes = models.TextField(max_length=1024, blank=True)
    plot_notes = models.TextField(max_length=1024, blank=True)
    logistics_notes = models.TextField(max_length=1024, blank=True)
    admin_notes = models.TextField(max_length=1024, blank=True)
    bank = models.DecimalField(max_digits=6, decimal_places=1, default=22.0)
    xp = models.DecimalField(max_digits=8, decimal_places=4, default=50.0)
    hp = models.PositiveIntegerField(default=25)
    is_alive = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    character_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    character_class = models.ForeignKey('Character_Class', null=True, on_delete=models.SET_NULL)
    character_race = models.ForeignKey('Character_Race', null=True, on_delete=models.SET_NULL, limit_choices_to={'is_pc_race': True})
    character_subrace = models.ForeignKey('Character_Subrace', null=True, on_delete=models.SET_NULL)
    rewrites_available = models.PositiveIntegerField(default=2)

    def get_absolute_url(self):
        return reverse('character:detail', kwargs={'pk': self.pk})

    def get_spent_xp(self):
        spent_xp = Decimal('0.0')
        for character_skill in self.character_skill_set.all():
            spent_xp += Decimal(character_skill.get_total_cost())
        return spent_xp

    def get_free_xp(self):
        return (self.xp - self.get_spent_xp())

    def calculate_hp(self):
        self.hp = 25
        xHP_skill = Skill.objects.get(abbrev='xHP') #Expects xHP to be in DB or fails
        try:
            character_xHP = self.character_skill_set.get(skill=xHP_skill).multiplier
        except:
            character_xHP = 0
        self.hp += (character_xHP * 2)
        return self.hp

    def calculate_xp(self):
        self.xp = Decimal('50.0') + self.calculate_earned_xp()
        return self.xp

    def calculate_character_hours(self):
        self.character_hours = Decimal('0.0')
        for player_event in self.player_events_set.all():
            self.character_hours += player_event.calculate_character_hours()
        return self.character_hours

    def calculate_earned_xp(self):
        earned_xp = Decimal('0.0')
        character_hours = self.calculate_character_hours()
        if character_hours <= 50:
            earned_xp += character_hours
        elif character_hours <= 200:
            earned_xp = 50 + ((character_hours-50)/2)
        elif character_hours <= 500:
            earned_xp = 175 + ((character_hours-200)/4)
        elif character_hours <= 900:
            earned_xp = 250 + ((character_hours-500)/8)
        elif character_hours <= 1700:
            earned_xp = 300 + ((character_hours-900)/16)
        elif character_hours <= 3300:
            earned_xp = 350 + ((character_hours-1700)/32)
        else:
            earned_xp = 400 + ((character_hours-3300)/64)
        return earned_xp

    def __str__(self):
        if (self.name != 'Unnamed'):
            return self.name
        else:
            return 'Unnamed ({0} {1})'.format(self.user.first_name, self.user.last_name)

    def get_name_with_player(self):
        return '{0} {1} - {2}'.format(self.user.first_name, self.user.last_name, self.name)


class Character_Skill(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE)
    skill = models.ForeignKey('skill.Skill', on_delete=models.CASCADE)
    multiplier = models.PositiveIntegerField(default=1)
    option = models.ForeignKey('skill.Skill_Option', null=True, blank=True, on_delete=models.SET_NULL)

    def get_cost(self):
        return (self.skill.get_cost_for_character(self.character))

    def get_total_cost(self):
        return (self.get_cost() * self.multiplier)

    def __str__(self):
        return '{0} - {1}'.format(self.character, self.skill)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Character.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
