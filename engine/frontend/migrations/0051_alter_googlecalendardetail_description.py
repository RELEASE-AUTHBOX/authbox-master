# Generated by Django 4.2 on 2024-09-20 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0050_alter_googlecalendar_file_path_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googlecalendardetail',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]