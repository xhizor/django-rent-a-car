# Generated by Django 2.0.7 on 2018-08-22 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='end_date',
            field=models.CharField(max_length=20),
        ),
    ]
