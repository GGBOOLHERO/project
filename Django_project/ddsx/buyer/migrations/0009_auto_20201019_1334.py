# Generated by Django 2.2.1 on 2020-10-19 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0008_checkemail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkemail',
            old_name='check_word',
            new_name='code',
        ),
    ]
