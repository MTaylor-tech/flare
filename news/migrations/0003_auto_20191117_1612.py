# Generated by Django 2.2.6 on 2019-11-17 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20191116_1022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article_slug',
            new_name='slug',
        ),
    ]
