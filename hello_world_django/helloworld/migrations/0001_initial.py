# Generated by Django 4.2.8 on 2024-04-02 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('device_idx', models.AutoField(primary_key=True, serialize=False)),
                ('device_name', models.CharField(default='none', max_length=30, unique=True)),
                ('device_profile_name', models.CharField(default='none', max_length=30)),
            ],
        ),
    ]
