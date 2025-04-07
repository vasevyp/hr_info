"""модели данных по персоналу"""

from django.db import models
from django.utils import timezone



class Department(models.Model):
    """таблица отделов компании"""

    code = models.CharField(max_length=20, unique=True, verbose_name="Код отдела")
    name = models.CharField(max_length=100, unique=True, verbose_name="Отдел")
    description = models.TextField(null=True, blank=True, default="Без описания")
    manager_job_title = models.CharField(
        max_length=30, verbose_name="Должность руководителя", null=True, blank=True
    )
    manager_last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    manager_first_name = models.CharField(max_length=30, verbose_name="Имя")
    manager_middle_name = models.CharField(
        max_length=30, verbose_name="Отчество", null=True, blank=True
    )
    created_date = models.DateField(auto_now_add=True, verbose_name="Создан", null=True)
    updated_date = models.DateField(auto_now=True, verbose_name="Изменен", null=True)

    def __str__(self):
        return self.name

    class Meta:
        """описание Департаментов"""

        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"


class Employee(models.Model):
    """таблица сотрудников"""

    # Основная информация
    code = models.CharField(max_length=20, unique=True, verbose_name="Код сотрудника")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Отчество"
    )
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    thumb = models.ImageField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=[("M", "Мужской"), ("F", "Женский")], verbose_name="Пол"
    )
    birthday = models.DateField(verbose_name="Дата рождения")
    place_of_birth = models.CharField(
        max_length=100, blank=True, verbose_name="Место рождения"
    )

    # Паспортные данные
    passport = models.CharField(
        max_length=50, blank=True, verbose_name="Паспортные данные"
    )

    # Адреса
    address = models.CharField(max_length=255, verbose_name="Адрес проживания")
    provincial_address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Домашний адрес"
    )

    # Контактная информация
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    # Гражданство и статус
    citizenship = models.CharField(max_length=50, verbose_name="Гражданство")
    civil_status = models.CharField(
        max_length=20,
        choices=[
            ("single", "Холост/Не замужем"),
            ("married", "Женат/Замужем"),
            ("divorced", "Разведен(а)"),
        ],
        blank=True,
        null=True,
        verbose_name="Семейное положение",
    )

    # Профессиональная информация
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, verbose_name="Отдел"
    )
    profession = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Профессия"
    )
    position = models.CharField(max_length=100, verbose_name="Должность")
    hire_date = models.DateField(verbose_name="Дата приема на работу")
    contract_expiration = models.DateField(
        blank=True, null=True, verbose_name="Дата окончания контракта"
    )
    salary_type = models.CharField(
        max_length=10,
        choices=[
            ("M", "Месячный оклад"),
            ("H", "Часовая ставка"),
        ],
        verbose_name="Тип оплаты",
    )
    salary_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Оклад, руб /тарифная ставка, руб в час.",
    )

    # Дополнительная информация
    remarks = models.TextField(blank=True, null=True, verbose_name="Примечание")

    # Даты создания и обновления
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

    class Meta:
        """для админки"""

        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

 
    def total_hours_worked(self):
        """вывод отработанных часов на экран"""
        from hr_cost.models import WorkTime

        today = timezone.now()
        work_times = WorkTime.objects.filter(
            employee=self, date__month=today.month, date__year=today.year
        )
        total = sum(work_time.hours_worked for work_time in work_times)
        return total

    @property
    def employee(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

class Vacation(models.Model):
    """таблицы отпусков сотрудников"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    code=models.IntegerField(verbose_name='Код')
    planned_start_date = models.DateField('Плановый день начала отпуска')
    planned_end_date = models.DateField('Плановый день окончания отпуска')
    actual_start_date = models.DateField('Фактический день начала отпуска', null=True, blank=True)
    actual_end_date = models.DateField('Фактический день окончания отпуска', null=True, blank=True)
    
    planned_days=models.PositiveIntegerField(
        'Количество дней отпуска по плану', blank=True, null=True
        
    )
    remaining_days = models.IntegerField('Количество дней отпуска осталось', default=0)
    
    class Meta:
        """описание таблицы Отпусков"""
        verbose_name = 'Отпуск'
        verbose_name_plural = 'Отпуска'
        ordering = ['employee', 'planned_start_date']
    
    def __str__(self):
        return f"Отпуск {self.employee} ({self.planned_start_date} - {self.planned_end_date})"
    
    def save(self, *args, **kwargs):
        # Автоматически вычисляем оставшиеся дни при сохранении
        self.planned_days=(self.planned_end_date - self.planned_start_date).days + 1
        if self.actual_start_date and self.actual_end_date:
            used_days = (self.actual_end_date - self.actual_start_date).days + 1
            self.remaining_days = self.planned_days - used_days
        else:
            self.remaining_days = self.planned_days
        super().save(*args, **kwargs)        

class SalaryHistory(models.Model):
    """таблица исторической зарплаты сотрудников"""

    period=models.DateField(verbose_name="Период")
    code = models.CharField(max_length=20, verbose_name="Код сотрудника")
    employee = models.CharField(max_length=150, verbose_name="Сотрудник")
    accrued_salary = models.FloatField(
        verbose_name="Начислено за отработанное время, руб."
    )
    bonus = models.FloatField(verbose_name="Бонус, руб.")
    salary = models.FloatField(verbose_name="Зарплата, руб.")
     # Даты создания и обновления
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    

    def __str__(self):
        return f"{self.employee}"

    class Meta:
        """описание таблицы  hr_data_salaryhistory"""

        verbose_name = "историческия зарплата"
        verbose_name_plural = "История-Зарплата"
        ordering = ['-period', 'employee']

class TimeSheetHistory(models.Model):
    """таблица исторического табеля сотрудников"""
    period=models.DateField(verbose_name="Период")
    date = models.DateField(verbose_name="Дата", default='2025-01-01')
    code = models.CharField(max_length=20, verbose_name="Код сотрудника")
    employee = models.CharField(max_length=150, verbose_name="Сотрудник")
    timesheet_data =models.CharField(max_length=20, verbose_name="Табель")
     # Даты создания и обновления
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    

    def __str__(self):
        return f"{self.employee}"

    class Meta:
        """описание таблицы hr_data_timesheethistory"""

        verbose_name = "исторический табель"
        verbose_name_plural = "История-Табель"
        ordering = ['-period', 'employee', '-date']
