# Generated by Django 4.0.4 on 2022-05-28 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_bot', '0003_alter_secondaryfile_secondary_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcefile',
            name='file_name',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
