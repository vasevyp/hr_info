"""модели данных по операциям с персоналом"""

from django.db import models

class UploadTimeSheet(models.Model):
    """таблица загрузки табеля сотрудников"""

    code = models.CharField(max_length=20, verbose_name="Код сотрудника")
    employee = models.CharField(max_length=150, verbose_name="Сотрудник")
    date = models.DateField(verbose_name="Дата")
    timesheet_data =models.CharField(max_length=20, verbose_name="Час/Инфо")


    def __str__(self):
        return f"{self.employee} - {self.date}: {self.timesheet_data}"

    class Meta:
        """описание для таблицы загрузки табеля"""

        verbose_name = "табель сотрудника"
        verbose_name_plural = "Табель Загрузка"

class TimeSheet(models.Model):
    """таблица табеля сотрудников"""

    code = models.CharField(max_length=20, verbose_name="Код сотрудника")
    employee = models.CharField(max_length=150, verbose_name="Сотрудник")
    date = models.DateField(verbose_name="Дата")
    timesheet_data =models.CharField(max_length=20, verbose_name="Табель сотрудника")


    def __str__(self):
        return f"{self.employee} - {self.date}: {self.timesheet_data}"

    class Meta:
        """описание для таблицы табеля сотрудника"""

        verbose_name = "табель сотрудника"
        verbose_name_plural = "Табель общий сотрудников"

class WorkTime(models.Model):
    """таблица отработанного времени сотрудником"""

    code = models.CharField(max_length=20, verbose_name="Код сотрудника")
    employee = models.CharField(max_length=150, verbose_name="Сотрудник")
    date = models.DateField(verbose_name="Дата")
    hours_worked = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Отработано часов"
    )

    def __str__(self):
        return f"{self.employee} - {self.date}: {self.hours_worked} часов"

    class Meta:
        """описание для таблицы тработанного времени"""

        verbose_name = "сотрудника"
        verbose_name_plural = "Табель рабочего времени"

class TimeSheetAbsence(models.Model):
    """таблица табеля отсутствующих сотрудников"""

    code = models.CharField(max_length=20, verbose_name="Код сотрудника")
    employee = models.CharField(max_length=150, verbose_name="Сотрудник")
    date = models.DateField(verbose_name="Дата")
    timesheet_data =models.CharField(max_length=20, verbose_name="Инфо")


    def __str__(self):
        return f"{self.employee} - {self.date}: {self.timesheet_data}"

    class Meta:
        """описание для таблицы загрузки табеля"""

        verbose_name = "табель сотрудника"
        verbose_name_plural = "Табель отсутствия сотрудников"        


class Bonus(models.Model):
    """таблица бонусов сотрудников"""

    code = models.CharField(max_length=20, unique=True, verbose_name="Код сотрудника")
    employee = models.CharField(max_length=150, verbose_name="Сотрудник")
    bonus = models.FloatField(verbose_name="Бонус, руб.", default=0)

    def __str__(self):
        return f"{self.employee}"

    class Meta:
        """описание таблицы Бонусов"""

        verbose_name = "Бонус"
        verbose_name_plural = "Бонусы"


class Salary(models.Model):
    """таблица зарплаты сотрудников"""

    code = models.CharField(max_length=20, unique=True, verbose_name="Код сотрудника")
    employee = models.CharField(max_length=150, verbose_name="Сотрудник")
    accrued_salary = models.FloatField(
        verbose_name="Начислено за отработанное время, руб."
    )
    bonus = models.FloatField(verbose_name="Бонус, руб.")
    salary = models.FloatField(verbose_name="Зарплата, руб.")

    def __str__(self):
        return f"{self.employee}"

    class Meta:
        """описание таблицы Зарплата"""

        verbose_name = "Зарплата"
        verbose_name_plural = "Зарплата"
