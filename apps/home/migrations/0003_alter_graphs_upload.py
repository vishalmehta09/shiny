# Generated by Django 4.0.5 on 2022-06-29 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_graphs_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphs',
            name='upload',
            field=models.FileField(upload_to='csv_files'),
        ),
    ]