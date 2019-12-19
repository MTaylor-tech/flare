from django.db import models

# Create your models here.
class Skill(models.Model):
    SKILL_TYPES = (
        ('AW', 'At-Will'),
        ('Pa', 'Passive'),
        ('Pr', 'Production'),
        ('PD', 'Per-Day')
    )
    name = models.CharField(max_length=50)
    abbrev = models.SlugField(max_length=5)
    description = models.TextField(blank=True)
    has_options = models.BooleanField(default=False)
    is_racial = models.BooleanField(default=False)
    has_racial_cost = models.BooleanField(default=False)
    is_bonus_skill = models.BooleanField(default=False)
    prereq = models.ManyToManyField('self', null=True, blank=True, symmetrical=False, related_name='prereq_of')
    replaces_skills = models.ManyToManyField('self', null=True, blank=True, symmetrical=False, related_name='replaced_by')
    multiplier = models.BooleanField(default=False)
    is_production_skill = models.BooleanField(default=False)
    skill_type = models.CharField(max_length=2, choices=SKILL_TYPES)
    skill_category = models.ForeignKey('Skill_Category', null=True, on_delete=models.SET_NULL)
    has_bonus_cost = models.BooleanField(default=False)
    replacement_is_mandatory = models.BooleanField(default=False)
    available_to_races = models.ManyToManyField('character.Character_Race', blank=True)

    def get_cost_for_class(self, character_class):
        skill_cost = Skill_Cost.objects.get(skill=self,character_class=character_class)
        return skill_cost.cost

    def get_bonus_cost_for_class(self, character_class):
        skill_cost = Bonus_Cost.objects.get(skill=self,character_class=character_class)
        return skill_cost

    def get_racial_cost_for_class_and_race(self, character_class, character_race):
        if self.has_racial_cost:
            try:
                skill_cost = Racial_Cost.objects.get(skill=self,character_class=character_class,character_race=character_race)
                return skill_cost.cost
            except:
                skill_cost = self.get_cost_for_class(character_class)
                return skill_cost
        else:
            skill_cost = self.get_cost_for_class(character_class)
            return skill_cost

    def get_cost_for_character(self, character):
        racial_cost = 9999
        bonus_cost = 9999
        base_cost = 9999
        if self.has_racial_cost:
            racial_cost = self.get_racial_cost_for_class_and_race(character.character_class, character.character_race)
        if self.has_bonus_cost:
            test_bonus_cost = self.get_bonus_cost_for_class(character.character_class)
            mPrf = Skill.objects.get(abbrev='MPrf')
            try:
                character_skills = character.character_skill_set.filter(skill=mPrf).all()
                #raise ValueError('Character Skills')
                for cs in character_skills:
                    so = cs.option
                    if cs.option in test_bonus_cost.skill_option.all():
                        bonus_cost = test_bonus_cost.cost
                        #raise ValueError('bonus_cost')
            except:
                #raise ValueError('Except')
                pass
        base_cost = self.get_cost_for_class(character.character_class)
        return min(racial_cost, bonus_cost, base_cost)

    def __str__(self):
        return self.abbrev

class Skill_Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Skill_Cost(models.Model):
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    character_class = models.ForeignKey('character.Character_Class', on_delete=models.CASCADE)
    cost = models.PositiveIntegerField(default=999)

    def __str__(self):
        return '{0}|{1}'.format(self.skill, self.character_class.abbrev)

class Racial_Cost(models.Model):
    character_race = models.ForeignKey('character.Character_Race', on_delete=models.CASCADE,null=True)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE,null=True)
    character_class = models.ForeignKey('character.Character_Class', on_delete=models.CASCADE,null=True)
    cost = models.PositiveIntegerField(default=999)

    def __str__(self):
        return '{0}|{1}({2})'.format(self.skill, self.character_class.abbrev, self.character_race)

class Bonus_Cost(models.Model):
    skill_option = models.ManyToManyField('Skill_Option', blank=True)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE,null=True)
    character_class = models.ForeignKey('character.Character_Class', on_delete=models.CASCADE,null=True)
    cost = models.PositiveIntegerField(default=999)

    def __str__(self):
        return '{0}|{1}(Bonus)'.format(self.skill, self.character_class.abbrev, self)

class Skill_Option_Category(models.Model):
    name = models.CharField(max_length=50)
    skill = models.ManyToManyField('Skill',null=True, related_name='category')

    def __str__(self):
        return self.name


class Skill_Option(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('Skill_Option_Category', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=300, blank=True)
    bonus_skill = models.ForeignKey('Skill', blank=True, null=True, on_delete=models.SET_NULL, limit_choices_to={'is_bonus_skill': True }, related_name='bonus_for_prof')
    subcategory = models.CharField(max_length=50, blank=True)

    def __str__(self):
        if self.subcategory != '':
            return '{0}|{1} - {2}'.format(self.category, self.subcategory, self.name)
        else:
            return '{0} - {1}'.format(self.category, self.name)
