# Generated by Django 4.2 on 2023-04-09 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sathiuser',
            name='gender',
            field=models.CharField(max_length=6),
        ),
    ]
