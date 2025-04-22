from django.db import migrations


def truncate_long_country_codes(apps, schema_editor):
    UserProfile = apps.get_model('accounts', 'UserProfile')
    for profile in UserProfile.objects.all():
        if profile.country and len(str(profile.country)) > 2:
            profile.country = 'US'  
            profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_userprofile_full_name_alter_userprofile_country_and_more'),
    ]

    operations = [
        migrations.RunPython(truncate_long_country_codes),
    ]
