# Generated by Django 2.2.5 on 2021-04-10 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauthen', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='city',
            new_name='locality',
        ),
    ]
