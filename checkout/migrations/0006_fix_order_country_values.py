from django.db import migrations


def truncate_order_country_codes(apps, schema_editor):
    Order = apps.get_model('checkout', 'Order')
    for order in Order.objects.all():
        if order.country and len(str(order.country)) > 2:
            order.country = 'SE'
            order.save()


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_order_user_profile'),
    ]

    operations = [
        migrations.RunPython(truncate_order_country_codes),
    ]
