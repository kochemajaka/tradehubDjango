# Generated by Django 5.1 on 2024-10-27 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0016_alter_tasks_completedate'),
    ]

    operations = [
        migrations.CreateModel(
            name='KanbanDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transferDate', models.DateField()),
                ('carId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.cars')),
                ('stadeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.kanbancols')),
            ],
            options={
                'db_table': 'kanban_date',
            },
        ),
    ]
