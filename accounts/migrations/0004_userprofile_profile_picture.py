# Generated by Django 3.2.3 on 2021-06-25 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='userprofile'),
        ),
    ]
