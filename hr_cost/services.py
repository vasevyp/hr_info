import csv
import os
import calendar
import datetime
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from hr_data.models import Employee
from .models import (
    Salary,
    Bonus,
    WorkTime,
    UploadTimeSheet,
    TimeSheet,
    TimeSheetAbsence,
)

# Получаем текущий месяц и год
today = timezone.now()
current_month = today.month
current_year = today.year

# Сохраняем табель в CSV
def save_timesheet_to_csv(timesheet_data, dates, month, year):
    """Сохраняем табель в CSV в папку data_save + скачиваем на локальный пк"""
    # Создаем папку data_save, если её нет
    folder_path = os.path.join("data_save")
    os.makedirs(folder_path, exist_ok=True)

    # Формируем имя файла
    file_name = f"timesheet_{year}_{month:02d}.csv"
    file_path = os.path.join(folder_path, file_name)

    # Записываем данные в CSV
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="\t")

        # Заголовок таблицы
        # header = ['Сотрудник'] + dates
        header = ["Сотрудник"] + ["ID"] + ["Итого"] + [date["date"] for date in dates]
        writer.writerow(header)

        # Данные по сотрудникам
        for data in timesheet_data:
            row = (
                [data["employee"]]
                + [data["code"]]
                + [data["total_hours"]]
                + data["hours"]
            )
            writer.writerow(row)


def export_timesheet_csv(request):
    """скачиваем табель в формате CSV на локальный пк"""
    # Формируем имя файла
    file_name = f"timesheet_{current_year}_{current_month:02d}.csv"
    file_path = os.path.join("data_save", file_name)

    # Открываем файл и возвращаем его как ответ
    with open(file_path, "r", encoding="utf-8") as file:
        response = HttpResponse(file.read(), content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response


def export_timesheet_pdf(request):
    """скачиваем список сотрудников в формате pdf на локальный пк"""
    # Получаем данные для табеля
    employees = Employee.objects.all().order_by(
        "last_name", "first_name", "middle_name"
    )
    timesheet_data = []

    for employee in employees:
        work_times = WorkTime.objects.filter(
            code=employee.code, date__month=current_month, date__year=current_year
        ).order_by("date")
        total = sum(work_time.hours_worked for work_time in work_times)
        timesheet_data.append(
            {"employee": employee, "work_times": work_times, "total": total}
        )

    # Рендерим HTML-шаблон в строку
    html_string = render_to_string(
        "hr_cost/timesheet_pdf.html",
        {
            "timesheet_data": timesheet_data,
            "current_month": today.strftime("%B %Y"),
        },
    )

    # Создаем PDF-файл
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    # Возвращаем PDF как ответ
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="timesheet.pdf"'
    return response


def salary_calculation():
    """расчет/перерасчет заработной платы за отработанное время"""
    Salary.objects.all().delete()
    employees = Employee.objects.all()
    print("start salary_calculation")
   
    cal = calendar.Calendar()
    # рабочие дни в месяце
    working_days = len(
        [
            x
            for x in cal.itermonthdays2(current_year, current_month)
            if x[0] != 0 and x[1] < 5
        ]
    )

    for item in employees:
        name = item.employee
        worktime = WorkTime.objects.filter(code=item.code).aggregate(
            summa=Sum("hours_worked")
        )
        total_hours = worktime["summa"]
        print("000000", name, item.code, total_hours)
        # rate=''
        if total_hours is None:
            rate = 0
        elif item.salary_type == "H":
            rate = item.salary_rate * total_hours
        else:
            rate = item.salary_rate / (working_days * 8) * total_hours
        try:
            bonuses = Bonus.objects.get(code=item.code)
            bonus = bonuses.bonus
            # print('222', bonuses, bonuses.bonus)
        except Bonus.DoesNotExist:
            bonus = 0
            # print('333', bonus)
        Salary.objects.create(
            code=item.code,
            employee=f"{item.last_name} {item.first_name} {item.middle_name}",
            accrued_salary=rate,
            bonus=bonus,
            salary=float(rate) + float(bonus),
        )

    print(" salary_calculation - OK!!!")


def timesheet_save(request):
    """сохранение данных табеля из файла/(hr_cost_uploadtimesheet) в базу данных"""
    print("start run save_timesheet function")
    new_date = UploadTimeSheet.objects.last().date.strftime("%Y-%m-%d")
    print("new_date==", new_date, type(new_date))
    last_date = TimeSheet.objects.filter(date=new_date).first()
    print("last_date ==", last_date, type(last_date))
    if last_date is None:
        last_date = datetime.datetime.now()
    elif last_date:
        last_date = (
            TimeSheet.objects.filter(date=new_date).first().date.strftime("%Y-%m-%d")
        )
    else:
        last_date = datetime.datetime.now()

    print(f"new = {new_date}, last= {last_date}", type(new_date), type(last_date))
    if new_date == last_date:
        print("Double Date Uploading")
        double_upload = f"Данные табеля на дату {new_date} уже есть в базе данных !"
        return render(
            request,
            "hr_cost_upload/timesheet_upload.html",
            {"double_upload": double_upload},
        )
    else:
        print("Date NOT == Double")
        employees = UploadTimeSheet.objects.all()
        for employee in employees:

            try:
                TimeSheet.objects.create(
                    code=employee.code,
                    employee=employee.employee,
                    date=employee.date,
                    timesheet_data=employee.timesheet_data,
                )
                WorkTime.objects.create(
                    code=employee.code,
                    employee=employee.employee,
                    date=employee.date,
                    hours_worked=employee.timesheet_data,
                )
            except Exception as e:
                print(employee, employee.timesheet_data, e)
                TimeSheetAbsence.objects.create(
                    code=employee.code,
                    employee=employee.employee,
                    date=employee.date,
                    timesheet_data=employee.timesheet_data,
                )
        salary_calculation()
        
    return redirect("timesheet_list")


def export_salary_list_pdf(request):
    """Сохранить список зарплат сотрудников в формате pdf"""
    # Получаем список сотрудников
    employees = Salary.objects.all()

    # Рендерим HTML-шаблон в строку
    html_string = render_to_string(
        "hr_cost/salary_list_pdf.html", {"employees": employees, 'date_is': WorkTime.objects.last().date}
    )

    # Создаем PDF-файл
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    # Возвращаем PDF как ответ

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename= "employee_salary.pdf"'  #
    return response
def bonus_save(request):
    pass




