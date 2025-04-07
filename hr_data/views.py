"""views для данных по сотрудникам"""

from calendar import monthrange
import datetime
from datetime import date
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.db.models import Sum
from weasyprint import HTML

from hr_cost.models import WorkTime, Salary, Bonus, TimeSheet, TimeSheetAbsence
from hr_cost.forms import WorkTimeForm


from .models import Department, Employee, Vacation, SalaryHistory, TimeSheetHistory
from .forms import EmployeDepartmentForm, EmployeeSearchForm, DateSalaryInput


# Получаем текущий месяц и год
today = timezone.now()
current_month = today.month
current_year = today.year


# Create your views here.
def index(request):
    return render(request, "hr_data/index.html")


def main(request):
    """вывод данных по персоналу на главной странице"""
    context = {}
    total_count = ""
    total_days = ""
    total_hours = ""
    total_salary = 0
    total_bonus = 0
    total_accrued = 0
    ahpe = ""
    total_employee_cost = 0
    total_count = Employee.objects.all().count()
    last_date = WorkTime.objects.last()

    if last_date:
        last_date = WorkTime.objects.last().date
        total_days = WorkTime.objects.all().count()
        total_hours = WorkTime.objects.all().aggregate(summa=Sum("hours_worked"))
        total_hours = total_hours["summa"]
        total_accrued = Salary.objects.all().aggregate(summa=Sum("accrued_salary"))
        total_accrued = total_accrued["summa"]
        total_bonus = Salary.objects.all().aggregate(summa=Sum("bonus"))
        total_bonus = total_bonus["summa"]
        total_salary = Salary.objects.all().aggregate(summa=Sum("salary"))
        total_salary = total_salary["summa"]
        print(type(total_salary))
        if total_salary is None:
            total_employee_cost = 0
        else:
            total_employee_cost = total_salary * 1.3
        ahpe = total_hours / total_days
        context = {
            "total_count": total_count,
            "total_days": total_days,
            "total_hours": total_hours,
            "total_salary": total_salary,
            "total_bonus": total_bonus,
            "total_accrued": total_accrued,
            "ahpe": ahpe,
            "total_employee_cost": total_employee_cost,  # Предельная база (в рублях) 2 759 000 (30% с выплаты в пределах лимита базы), 15,1% – с выплаты свыше лимита базы
            "yesterday": last_date,
        }
    else:
        context = {
            "yesterday": today,
            "nodata": "- данные не введены",
        }
    return render(request, "hr_data/main.html", context)


# список отделов
class DepartmentList(ListView):
    """вывод списка отделов"""

    model = Department
    template_name = "hr_data/dapartment_list.html"
    context_object_name = "items"


# список сотрудников отдела
def employee_list(request):
    """eployee list, Вывод списка сотрудников выбранного отдела"""
    # сщздаем переменные для хранения данных внутри функции
    employees_dep = ""
    department = ""
    select_except = False
    # форма выборки сотрудников отдела по названи. отдела
    form = EmployeDepartmentForm
    if request.method == "POST":
        department = request.POST.get("department_name")
        # убрать лишние символы с обеих сторон строки
        department = department.strip()
        # делаем выборку списка сотрудников по департаменту
        try:
            item = Department.objects.get(name=department)
            print(item, "department=", department)
            employees_dep = Employee.objects.filter(department=item)
        # обрабатываем ошибку в веденном названии отдела
        except Department.DoesNotExist as e:
            select_except = "Название департамента не корректное"
            print(f"NO department == {department}", e)
            return render(
                request,
                "hr_form/employee_department.html",
                {"select_except": select_except, "department": department},
            )
    # Получаем все отделы
    objects = Department.objects.all()
    # Получаем всех сотрудников
    employees = Employee.objects.all().order_by(
        "last_name", "first_name", "middle_name"
    )
    return render(
        request,
        "hr_form/employee_department.html",
        {
            "employees": employees,
            "employees_dep": employees_dep,
            "form": form,
            "department": department,
            "objects": objects,
            "select_except": select_except,
        },
    )


def employee_detail(request, pk):
    """Детальная информация по сотруднику"""
    employee = Employee.objects.get(pk=pk)
    total_hours = WorkTime.objects.filter(code=employee.code).aggregate(
        summa=Sum("hours_worked")
    )
    total_hours = total_hours["summa"]
    current_salary = Salary.objects.filter(code=employee.code).aggregate(
        summa=Sum("salary")
    )
    current_salary = current_salary["summa"]
    abcences = TimeSheetAbsence.objects.filter(code=employee.code)
    vacations = Vacation.objects.filter(code=employee.code)
    return render(
        request,
        "hr_data/employee_detail.html",
        {
            "employee": employee,
            "abcences": abcences,
            "vacations": vacations,
            "total_hours": total_hours,
            "current_salary": current_salary,
        },
    )


def employee_vacation_list(request):
    """вывод списка отпусков"""
    employees = Vacation.objects.all()
    context = {
        "employees": employees,
    }
    return render(request, "hr_data/employee_vacation_list.html", context)


def export_employee_list_pdf(request):
    """Сохранить список сотрудников в формате pdf"""
    # Получаем список сотрудников
    employees = Employee.objects.all()

    # Рендерим HTML-шаблон в строку
    html_string = render_to_string(
        "hr_data/employee_list_pdf.html", {"employees": employees}
    )

    # Создаем PDF-файл
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    # Возвращаем PDF как ответ

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename= "employee_list.pdf"'
    return response


def employee_search(request):
    """Поиск сотрудника по фамилии"""
    form = EmployeeSearchForm(request.GET or None)
    employees = []

    if form.is_valid():
        last_name = form.cleaned_data.get("last_name")
        if last_name:
            # Поиск сотрудников по фамилии (без учета регистра)
            employees = Employee.objects.filter(
                last_name__icontains=last_name.capitalize()
            )

    return render(
        request,
        "hr_data/employee_search.html",
        {
            "form": form,
            "employees": employees,
        },
    )


def history_salary(request):
    """сохранение зарплаты за месяц в базу прошлых периодов"""
    form = DateSalaryInput()

    ft_date = SalaryHistory.objects.first().period
    lt_date = SalaryHistory.objects.last().period

    if request.method == "POST":

        year = request.POST.get("year")
        month = request.POST.get("month")
        period = datetime.date(int(year), int(month), 1)
        # делаем сохранение зарплаты за месяц в исторические данные
        try:
            items = Salary.objects.all()
            print(period, "salary ==")
            history_period = SalaryHistory.objects.filter(period=period).first()
            if history_period:
                db_period = SalaryHistory.objects.filter(period=period).first().period
            else:
                db_period = history_period
            print("history_period ==", history_period, db_period)
            for item in items:
                if period != db_period:
                    SalaryHistory.objects.get_or_create(
                        period=period,
                        employee=item.employee,
                        code=item.code,
                        accrued_salary=item.accrued_salary,
                        bonus=item.bonus,
                        salary=item.salary,
                    )
                else:
                    select_except = (
                        f"Что-то не так!!! Вы повторно сохраняете данные за {period}"
                    )
                    return render(
                        request,
                        "hr_data_history/history_salary.html",
                        {"select_except": select_except},
                    )
            # удалаяем данные за месяц из текущих баз по зарплате и бонусу
            # Salary.objects.all().delete()
            # Bonus.objects.all().delete()
        # обрабатываем ошибку в веденном названии отдела
        except Exception as e:
            print("SalaryHisory Exceptin ==", e)
            select_except = (
                f"Что-то не так??? Вы повторно сохраняете данные за {period}"
            )
            return render(
                request,
                "hr_data_history/history_salary.html",
                {"select_except": select_except},
            )
    # Получаем все исторические зарплаты
    objects = SalaryHistory.objects.all()

    return render(
        request,
        "hr_data_history/history_salary.html",
        {
            "form": form,
            "salary_list": objects,
            "first_date": ft_date,
            "last_date": lt_date,
        },
    )


def history_timesheet(request):
    """сохранение табеля за месяц в базу прошлых периодов"""
    form = DateSalaryInput()

    ft_date = TimeSheetHistory.objects.first().period
    lt_date = TimeSheetHistory.objects.last().period

    if request.method == "POST":

        year = request.POST.get("year")
        month = request.POST.get("month")
        period = datetime.date(int(year), int(month), 1)
        # делаем сохранение зарплаты за месяц в исторические данные
        try:
            items = TimeSheet.objects.all()
            print(period, "timesheet ==")
            history_period = TimeSheetHistory.objects.filter(period=period).first()
            if history_period:
                db_period = (
                    TimeSheetHistory.objects.filter(period=period).first().period
                )
            else:
                db_period = history_period
            print("history_period ==", history_period, db_period)
            for item in items:
                if period != db_period:
                    TimeSheetHistory.objects.get_or_create(
                        period=period,
                        date=item.date,
                        employee=item.employee,
                        code=item.code,
                        timesheet_data=item.timesheet_data,
                    )
                else:
                    select_except = (
                        f"Что-то не так!!! Вы повторно сохраняете данные за {period}"
                    )
                    return render(
                        request,
                        "hr_data_history/history_timesheet.html",
                        {"select_except": select_except},
                    )
            # удаляем данные из текущих таблиц
            # TimeSheet.objects.all().delete()
            # TimeSheetAbsence.objects.all().delete()
            # WorkTime.objects.all().delete()
        # обрабатываем ошибку в веденном названии отдела
        except Exception as e:
            print("SalaryHisory Exceptin ==", e)
            select_except = (
                f"Что-то не так??? Вы повторно сохраняете данные за {period}"
            )
            return render(
                request,
                "hr_data_history/history_timesheet.html",
                {"select_except": select_except},
            )
    # Получаем все исторические зарплаты
    objects = TimeSheetHistory.objects.all()[:500]

    return render(
        request,
        "hr_data_history/history_timesheet.html",
        {
            "form": form,
            "timesheet_list": objects,
            "first_date": ft_date,
            "last_date": lt_date,
        },
    )


def timesheet_select(request):
    """вывод таблицы табеля за заданный месяц/период"""
    form = DateSalaryInput()
    # Создаем список для хранения данных табеля
    timesheet_data = []
    dates = []
    year = today.year
    month = today.month

    if request.method == "POST":
        # получаем данные из формы
        year = request.POST.get("year")
        month = request.POST.get("month")
        period = datetime.date(int(year), int(month), 1)
        # выводим данные табеля за месяц из исторических данных
        try:
            # Получаем всех сотрудников
            employees = Employee.objects.all().order_by(
                "last_name", "first_name", "middle_name"
            )

            # Генерация списка дат для выбираемого/заданного месяца
            _, num_days = monthrange(int(year), int(month))

            dates = []
            for day in range(1, num_days + 1):
                current_date = date(int(year), int(month), day)
                weekday = current_date.weekday()  # Понедельник = 0, Воскресенье = 6
                dates.append(
                    {
                        "date": f"{day:02d}",
                        "weekday": weekday,  # Добавляем информацию о дне недели
                    }
                )

            for employee in employees:
                # Получаем отработанные периоды для выбранного месяца
                work_times = TimeSheetHistory.objects.filter(
                    code=employee.code, period=period
                )

                # Создаем словарь для хранения данных по дням
                employee_data = {
                    "employee": f"{employee.last_name} {employee.first_name} {employee.middle_name}",
                    "code": f"{employee.code}",
                    "hours": [""]
                    * num_days,  # Инициализируем список пустыми значениями
                }
                # Заполняем данные по дням
                for work_time in work_times:
                    day = work_time.date.day - 1  # Индекс дня в списке
                    employee_data["hours"][day] = str(work_time.timesheet_data)

                timesheet_data.append(employee_data)
        except Exception as e:
            print(e)

    return render(
        request,
        "hr_data_history/timesheet select .html",
        {
            "timesheet_data": timesheet_data,
            "dates": dates,
            "current_month": datetime.date(int(year), int(month), 1),
            "form": form,  # Передаем форму в шаблон
        },
    )


def salary_select(request):
    """вывод из исторических данных зарплаты по сотрудникам за выбранный месяц"""
    form = DateSalaryInput()
    # получаем данные из формы
    current_date = today
    salary_employees = ""
    if request.method == "POST":
        year = request.POST.get("year")
        month = request.POST.get("month")
        period = datetime.date(int(year), int(month), 1)

        # выводим данные табеля за месяц из исторических данных
        try:
            salary_employees = SalaryHistory.objects.filter(period=period)
            current_date = period

        except Exception as e:
            print(e)
    # employee = (employee.employee for employee in salary_employees)
    return render(
        request,
        "hr_data_history/salary_select.html",
        {"items": salary_employees, "form": form, "current_date": current_date},
    )


def main_history_select(request):
    """вывод из исторических данных информации/Dashbord за выбранный месяц"""
    form = DateSalaryInput()
    period = timezone.now()
    total_count = ""
    total_days = ""
    total_hours = ""
    total_salary = 0
    total_bonus = 0
    total_accrued = 0
    ahpe = ""
    total_employee_cost = 0
    # получаем данные из формы
    if request.method == "POST":
        year = request.POST.get("year")
        month = request.POST.get("month")
        period = datetime.date(int(year), int(month), 1)

        # исторические данные за период
        main_timesheet_history = TimeSheetHistory.objects.filter(period=period)
        main__salary_history = SalaryHistory.objects.filter(period=period)

        # подсчет отработанных человеко-дней за период
        list_days = []
        for item in main_timesheet_history:
            if item.timesheet_data.isdigit():
                list_days.append(item.timesheet_data)
        total_days = len(list_days)

        # получение исторических данных
        total_count = main__salary_history.count()
        total_hours = TimeSheetHistory.objects.filter(period=period).aggregate(
            summa=Sum("timesheet_data")
        )
        total_hours = total_hours["summa"]
        if total_days != 0:
            ahpe = total_hours / total_days
        else:
            ahpe = 0
        total_accrued = SalaryHistory.objects.filter(period=period).aggregate(
            summa=Sum("accrued_salary")
        )
        total_accrued = total_accrued["summa"]
        total_bonus = SalaryHistory.objects.filter(period=period).aggregate(
            summa=Sum("bonus")
        )
        total_bonus = total_bonus["summa"]
        total_salary = SalaryHistory.objects.filter(period=period).aggregate(
            summa=Sum("salary")
        )
        total_salary = total_salary["summa"]
        if total_salary:
            total_employee_cost = total_salary * 1.3

    content = {
        "form": form,
        "total_count": total_count,
        "total_days": total_days,
        "total_hours": total_hours,
        "ahpe": ahpe,
        "total_accrued": total_accrued,
        "total_bonus": total_bonus,
        "total_salary": total_salary,
        "total_employee_cost": total_employee_cost,
        "period": period,
    }
    return render(request, "hr_data_history/main_history_select.html", content)
