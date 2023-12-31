# Generated by Django 4.2 on 2023-10-14 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_remove_templateblock_variation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalsetting',
            name='name',
            field=models.SmallIntegerField(choices=[(1, 'Landing Page'), (2, 'Navigation')], default=None),
        ),
        migrations.AlterField(
            model_name='globalsetting',
            name='value',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='value'),
        ),
    ]
