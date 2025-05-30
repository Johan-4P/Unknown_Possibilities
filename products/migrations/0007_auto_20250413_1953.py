# Generated by Django 3.2.25 on 2025-04-13 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0006_alter_tarotcard_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarotcard',
            name='categories',
            field=models.ManyToManyField(related_name='tarot_cards', to='products.Category'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reading_type', models.CharField(choices=[('tarot', 'Tarot Reading'), ('rune', 'Rune Reading'), ('oracle', 'Oracle Reading')], max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
