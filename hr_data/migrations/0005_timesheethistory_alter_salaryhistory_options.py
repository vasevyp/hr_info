# Generated by Django 5.1.5 on 2025-04-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_data', '0004_alter_salaryhistory_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheetHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.DateField(verbose_name='Период')),
                ('code', models.CharField(max_length=20, verbose_name='Код сотрудника')),
                ('employee', models.CharField(max_length=150, verbose_name='Сотрудник')),
                ('timesheet_data', models.CharField(max_length=20, verbose_name='Табель сотрудника')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'исторический табель',
                'verbose_name_plural': 'История-Табель',
                'ordering': ['-period', 'employee'],
            },
        ),
        migrations.AlterModelOptions(
            name='salaryhistory',
            options={'ordering': ['-period', 'employee'], 'verbose_name': 'историческия зарплата', 'verbose_name_plural': 'История-Зарплата'},
        ),
    ]
