# Generated by Django 4.2 on 2023-04-25 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0002_alter_group_sath_id_alter_group_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='sath_id',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.CharField(choices=[('C', 'Complete'), ('I', 'Incomplete'), ('P', 'Pending')], max_length=1),
        ),
    ]
