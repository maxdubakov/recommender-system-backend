# Generated by Django 3.2.9 on 2021-11-13 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('beer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserBeer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField()),
                ('beer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beer.beer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='beers',
            field=models.ManyToManyField(through='user.UserBeer', to='beer.Beer'),
        ),
        migrations.AddField(
            model_name='user',
            name='categories',
            field=models.ManyToManyField(to='beer.Category'),
        ),
    ]
