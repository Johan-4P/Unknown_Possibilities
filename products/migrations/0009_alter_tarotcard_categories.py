# Generated by Django 3.2.25 on 2025-04-14 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20250413_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarotcard',
            name='categories',
            field=models.ManyToManyField(related_name='tarot_cards', to='products.Category'),
        ),
    ]
