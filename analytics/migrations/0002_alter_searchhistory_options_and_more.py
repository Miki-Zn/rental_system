# Generated by Django 5.2.1 on 2025-05-23 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='searchhistory',
            options={'ordering': ['-searched_at'], 'verbose_name_plural': 'Search History'},
        ),
        migrations.AlterModelOptions(
            name='viewhistory',
            options={'ordering': ['-viewed_at'], 'verbose_name_plural': 'View History'},
        ),
    ]
