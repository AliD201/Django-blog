# Generated by Django 3.1.7 on 2021-07-06 08:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('deal', '0002_deal_close_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='currency',
            field=models.CharField(default='$', max_length=4),
        ),
        migrations.AddField(
            model_name='deal',
            name='lost_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deal',
            name='won_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]