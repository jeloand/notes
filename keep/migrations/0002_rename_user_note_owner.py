# Generated by Django 3.2.5 on 2021-07-23 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keep', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='user',
            new_name='owner',
        ),
    ]
