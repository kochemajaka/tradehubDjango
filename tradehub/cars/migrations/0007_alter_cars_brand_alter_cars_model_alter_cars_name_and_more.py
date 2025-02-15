# Generated by Django 5.1 on 2024-10-05 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_alter_kanbancols_cross'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='brand',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='cars',
            name='model',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='cars',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='prebuycars',
            name='liquidRatio',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prebuycars',
            name='typeSourse',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
