# Generated by Django 4.2.22 on 2025-06-26 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0064_banner_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='position',
            field=models.PositiveIntegerField(choices=[(0, 'Default'), (1, 'Top'), (2, 'Middle Top'), (3, 'Middle Bottom'), (4, 'Bottom')], default=0),
        ),
    ]
