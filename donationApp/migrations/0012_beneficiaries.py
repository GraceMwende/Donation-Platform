# Generated by Django 4.0.3 on 2022-04-07 07:09

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationApp', '0011_rename_users_charity_charity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiaries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=30)),
            ],
        ),
    ]
