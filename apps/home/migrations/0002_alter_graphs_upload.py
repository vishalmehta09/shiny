# Generated by Django 3.2.6 on 2022-06-12 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphs',
            name='upload',
            field=models.FileField(upload_to='graphs'),
        ),
    ]
