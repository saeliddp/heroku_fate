# Generated by Django 2.2.6 on 2019-10-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('version2', '0003_auto_20191025_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respondent',
            name='age',
            field=models.CharField(default='None', max_length=50),
        ),
    ]
