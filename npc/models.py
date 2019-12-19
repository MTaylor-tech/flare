from django.db import models

# Create your models here.
class Monster_Type(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

class Monster(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(max_length=500, blank=True)
    costuming_notes = models.TextField(max_length=500, blank=True)
    special_abilities = models.TextField(max_length=1024, blank=True)
    attack = models.CharField(max_length=100, blank=True)
    intelligence = models.CharField(max_length=50, blank=True)
    hp = models.PositiveIntegerField(default=25)
    monster_type = models.ForeignKey('Monster_Type', null=True, on_delete=models.SET_NULL)
    killing_blow_active = models.BooleanField(default=False)
    typical_treasure = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    character_class = models.ForeignKey('character.Character_Class', null=True, on_delete=models.SET_NULL)
    character_race = models.ForeignKey('character.Character_Race', null=True, on_delete=models.SET_NULL)
    character_subrace = models.ForeignKey('character.Character_Subrace', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
