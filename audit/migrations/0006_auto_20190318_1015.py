# Generated by Django 2.0.7 on 2019-03-18 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0005_user_nid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='nid',
            field=models.IntegerField(default=2, primary_key=True, serialize=False),
        ),
    ]
