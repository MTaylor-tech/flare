from django.db import models

# Create your models here.
class Spell(models.Model):
    SCHOOLS = (
        ('E', 'Elemental'),
        ('S', 'Spirit'),
        ('N', 'None'),
        ('O', 'Other')
    )
    SUBSCHOOLS = (
        ('L', 'Light'),
        ('D', 'Darkness'),
        ('U', 'Unspecified')
    )
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1024, blank=True)
    school = models.CharField(max_length=1, choices=SCHOOLS, default='O')
    duration = models.CharField(max_length=100, blank=True)
    radius = models.CharField(max_length=100, blank=True)
    level = models.PositiveIntegerField(default=1)
    incantation = models.CharField(max_length=300, blank=True)
    is_damage_spell = models.BooleanField(default=False)
    is_healing_spell = models.BooleanField(default=False)
    damage_or_healing = models.PositiveIntegerField(default=0)
    subschool = models.CharField(max_length=1, choices=SUBSCHOOLS, default='U')

    def get_full_school(self):
        if (self.school == 'S'):
            return '{0}/{1}'.format(self.school, self.subschool)
        else:
            return self.school

    def __str__(self):
        return '{0}-{1}'.format(self.get_full_school(), self.name)
