# Generated by Django 4.1.4 on 2022-12-30 19:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('me_system', '0006_alter_monthlytable_num_not_accomplished_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
    ]