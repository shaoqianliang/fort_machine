# Generated by Django 2.0.7 on 2019-03-24 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0008_auto_20190321_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostgroup',
            name='group_bind_host',
            field=models.ManyToManyField(to='audit.HostUserBind'),
        ),
    ]
