# Generated by Django 4.1.4 on 2022-12-23 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me_system', '0002_frequency_alter_grant_currency_alter_grant_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='your name')),
                ('age', models.CharField(max_length=200, verbose_name='your age')),
                ('other', models.CharField(max_length=200, verbose_name='other details')),
            ],
        ),
    ]
