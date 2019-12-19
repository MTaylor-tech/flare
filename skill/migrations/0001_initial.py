# Generated by Django 2.2.6 on 2019-11-04 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('character', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abbrev', models.SlugField(max_length=5)),
                ('description', models.TextField(blank=True, max_length=300)),
                ('has_options', models.BooleanField(default=False)),
                ('is_racial', models.BooleanField(default=False)),
                ('has_racial_cost', models.BooleanField(default=False)),
                ('is_bonus_skill', models.BooleanField(default=False)),
                ('multiplier', models.BooleanField(default=False)),
                ('is_production_skill', models.BooleanField(default=False)),
                ('prereq', models.ManyToManyField(related_name='prereq_of', to='skill.Skill')),
                ('replaces_skills', models.ManyToManyField(related_name='replaced_by', to='skill.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='Skill_Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(default=999)),
                ('character_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character.Character_Class')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skill.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='Skill_Option_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skill.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='Skill_Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=300)),
                ('category', models.ForeignKey(blank=True, limit_choices_to={'skill': models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_available', to='skill.Skill')}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='skill.Skill_Option_Category')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_available', to='skill.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='Racial_Skill_Cost',
            fields=[
                ('skill_cost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='skill.Skill_Cost')),
                ('character_race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character.Character_Race')),
            ],
            bases=('skill.skill_cost',),
        ),
    ]