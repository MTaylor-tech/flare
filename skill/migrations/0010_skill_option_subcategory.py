# Generated by Django 2.2.6 on 2019-11-10 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0009_skill_available_to_races'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill_option',
            name='subcategory',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
