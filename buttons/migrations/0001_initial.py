# Generated by Django 2.0.2 on 2018-03-09 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('market_name', models.CharField(default='', max_length=30)),
                ('index', models.CharField(default='', max_length=50)),
            ],
        ),
    ]