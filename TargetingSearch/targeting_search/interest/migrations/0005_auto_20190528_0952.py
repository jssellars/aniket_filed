# Generated by Django 2.2 on 2019-05-28 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0004_auto_20190528_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawinterest',
            name='audience_size',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
