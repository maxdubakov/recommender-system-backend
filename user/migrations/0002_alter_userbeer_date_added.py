# Generated by Django 3.2.9 on 2021-11-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbeer',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
