# Generated by Django 2.2.1 on 2020-10-15 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0002_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='goods_total',
            field=models.FloatField(null=True),
        ),
    ]
