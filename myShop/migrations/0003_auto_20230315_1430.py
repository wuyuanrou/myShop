# Generated by Django 3.2.18 on 2023-03-15 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0002_auto_20230314_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='activity_people',
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_tickets_sold',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_tickets_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_sell',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='buyer_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='getter_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='phone',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seat',
            field=models.CharField(default='', max_length=100),
        ),
    ]
