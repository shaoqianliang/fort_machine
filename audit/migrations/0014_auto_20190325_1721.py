# Generated by Django 2.0.7 on 2019-03-25 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0013_auto_20190325_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='date',
            field=models.DateTimeField(auto_created=True, default='2019-01-01'),
        ),
    ]
