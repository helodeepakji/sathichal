# Generated by Django 4.2 on 2023-04-09 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_sathiuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sathiuser',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1),
        ),
    ]