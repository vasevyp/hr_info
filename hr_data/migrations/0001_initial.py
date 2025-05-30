# Generated by Django 5.1.5 on 2025-03-28 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Код отдела')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Отдел')),
                ('description', models.TextField(blank=True, default='Без описания', null=True)),
                ('manager_job_title', models.CharField(blank=True, max_length=30, null=True, verbose_name='Должность руководителя')),
                ('manager_last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('manager_first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('manager_middle_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Отчество')),
                ('created_date', models.DateField(auto_now_add=True, null=True, verbose_name='Создан')),
                ('updated_date', models.DateField(auto_now=True, null=True, verbose_name='Изменен')),
            ],
            options={
                'verbose_name': 'Департамент',
                'verbose_name_plural': 'Департаменты',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Код сотрудника')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('thumb', models.ImageField(blank=True, null=True, upload_to='')),
                ('gender', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=10, verbose_name='Пол')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('place_of_birth', models.CharField(blank=True, max_length=100, verbose_name='Место рождения')),
                ('passport', models.CharField(blank=True, max_length=50, verbose_name='Паспортные данные')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес проживания')),
                ('provincial_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Домашний адрес')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('citizenship', models.CharField(max_length=50, verbose_name='Гражданство')),
                ('civil_status', models.CharField(blank=True, choices=[('single', 'Холост/Не замужем'), ('married', 'Женат/Замужем'), ('divorced', 'Разведен(а)')], max_length=20, null=True, verbose_name='Семейное положение')),
                ('profession', models.CharField(blank=True, max_length=100, null=True, verbose_name='Профессия')),
                ('position', models.CharField(max_length=100, verbose_name='Должность')),
                ('hire_date', models.DateField(verbose_name='Дата приема на работу')),
                ('contract_expiration', models.DateField(blank=True, null=True, verbose_name='Дата окончания контракта')),
                ('salary_type', models.CharField(choices=[('M', 'Месячный оклад'), ('H', 'Часовая ставка')], max_length=10, verbose_name='Тип оплаты')),
                ('salary_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Оклад, руб /тарифная ставка, руб в час.')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr_data.department', verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
    ]
