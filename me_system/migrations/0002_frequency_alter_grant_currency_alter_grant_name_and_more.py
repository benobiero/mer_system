# Generated by Django 4.1.4 on 2022-12-18 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('me_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='grant',
            name='currency',
            field=models.CharField(default='KSh', max_length=100, verbose_name='Choose Currency'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Enter name'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='person_responsible',
            field=models.CharField(max_length=100, verbose_name='Person responsible'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='thematic_area',
            field=models.CharField(max_length=200, verbose_name='enter thematic'),
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
