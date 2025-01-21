# Generated by Django 4.2.5 on 2025-01-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='bookingslot',
            constraint=models.UniqueConstraint(fields=('date', 'time'), name='unique_slot_per_datetime'),
        ),
    ]
