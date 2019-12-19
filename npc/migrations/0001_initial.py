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
            name='Monster_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True, max_length=500)),
                ('costuming_notes', models.TextField(blank=True, max_length=500)),
                ('special_abilities', models.TextField(blank=True, max_length=1024)),
                ('attack', models.CharField(blank=True, max_length=100)),
                ('intelligence', models.CharField(blank=True, max_length=50)),
                ('hp', models.PositiveIntegerField(default=25)),
                ('killing_blow_active', models.BooleanField(default=False)),
                ('typical_treasure', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('character_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='character.Character_Class')),
                ('character_race', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='character.Character_Race')),
                ('character_subrace', models.ForeignKey(limit_choices_to={'character_race': models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='character.Character_Race')}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='character.Character_Subrace')),
                ('monster_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='npc.Monster_Type')),
            ],
        ),
    ]