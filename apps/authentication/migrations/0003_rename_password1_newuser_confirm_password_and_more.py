# Generated by Django 4.0.5 on 2022-06-29 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newuser',
            old_name='password1',
            new_name='confirm_password',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='normal_user',
        ),
        migrations.AddField(
            model_name='newuser',
            name='is_supervisor',
            field=models.BooleanField(default=False),
        ),
    ]