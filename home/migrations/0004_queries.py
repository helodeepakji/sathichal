# Generated by Django 4.2 on 2023-04-09 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_sathiuser_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='queries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('query', models.TextField()),
            ],
        ),
    ]
