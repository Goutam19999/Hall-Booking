# Generated by Django 5.2.2 on 2025-06-10 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_system', '0012_alter_booking_end_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
