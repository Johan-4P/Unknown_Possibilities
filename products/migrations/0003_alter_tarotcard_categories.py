# Generated by Django 3.2.25 on 2025-04-09 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20250409_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarotcard',
            name='categories',
            field=models.ManyToManyField(related_name='tarot_cards', to='products.Category'),
        ),
    ]
