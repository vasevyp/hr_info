# Generated by Django 5.1.5 on 2025-04-05 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_data', '0007_vacation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacation',
            name='planned_days',
            field=models.PositiveIntegerField(verbose_name='Количество дней отпуска по плану'),
        ),
    ]
