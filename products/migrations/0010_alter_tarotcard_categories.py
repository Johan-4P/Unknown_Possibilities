# Generated by Django 3.2.25 on 2025-04-14 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_tarotcard_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarotcard',
            name='categories',
            field=models.ManyToManyField(related_name='tarot_cards', to='products.Category'),
        ),
    ]
