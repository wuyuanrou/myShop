# Generated by Django 3.2.18 on 2023-03-22 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0003_auto_20230315_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='activity_price',
            field=models.IntegerField(default=0),
        ),
    ]
