# Generated by Django 5.1 on 2024-10-20 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0015_alter_dds_carid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='completeDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
