# Generated by Django 3.2.25 on 2025-04-14 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readings', '0002_booking_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='time',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('date', 'time', 'reading_type')},
        ),
    ]
