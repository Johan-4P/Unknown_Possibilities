from django.db import migrations

def fix_long_country_codes(apps, schema_editor):
    UserProfile = apps.get_model('accounts', 'UserProfile')
    for profile in UserProfile.objects.all():
        if profile.country and len(str(profile.country)) > 2:
            profile.country = 'SE'
            profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_userprofile_address_userprofile_county_and_more'),
]



    operations = [
        migrations.RunPython(fix_long_country_codes),
    ]
