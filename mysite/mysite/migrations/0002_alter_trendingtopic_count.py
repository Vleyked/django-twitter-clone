# Generated by Django 5.0.6 on 2024-07-14 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trendingtopic',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
