# Generated by Django 4.0.3 on 2022-04-05 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donationApp', '0009_alter_charity_charity_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BenefactorsStories',
            new_name='BenefactorsStory',
        ),
    ]
