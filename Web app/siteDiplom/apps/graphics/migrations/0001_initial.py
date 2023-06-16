# Generated by Django 4.2.1 on 2023-05-13 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pression', models.FloatField(verbose_name='Давление')),
                ('temperature', models.FloatField(verbose_name='Температура')),
                ('humidity', models.FloatField(verbose_name='Влажность')),
            ],
        ),
    ]