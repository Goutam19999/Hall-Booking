# Generated by Django 5.2.2 on 2025-06-06 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_system', '0003_hall_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
