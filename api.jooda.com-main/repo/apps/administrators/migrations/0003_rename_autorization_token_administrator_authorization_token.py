# Generated by Django 4.1.7 on 2023-04-11 11:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("administrators", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="administrator",
            old_name="autorization_token",
            new_name="authorization_token",
        ),
    ]
