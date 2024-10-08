# Generated by Django 4.2 on 2024-08-15 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0046_remove_aboutus_detail_post_remove_aboutus_icon'),
    ]
    

    operations = [
        migrations.AddField(
            model_name='googlecalendardetail',
            name='description',
            field=models.CharField(default=None, max_length=300, verbose_name='description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlecalendardetail',
            name='end',
            field=models.DateTimeField(default=None, verbose_name='date end'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlecalendardetail',
            name='event_id',
            field=models.CharField(default=None, max_length=100, verbose_name='google event ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlecalendardetail',
            name='location',
            field=models.CharField(default=None, max_length=300, verbose_name='location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlecalendardetail',
            name='start',
            field=models.DateTimeField(default=None, verbose_name='date start'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlecalendardetail',
            name='summary',
            field=models.CharField(default=None, max_length=300, verbose_name='Summary'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlecalendardetail',
            name='transparency',
            field=models.CharField(default=None, max_length=300, verbose_name='transparency'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googlecalendardetail',
            name='visibility',
            field=models.CharField(default=None, max_length=300, verbose_name='visibility'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='googlecalendar',
            name='file_path_doc',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='google calendar credentials path'),
        ),
    ]
