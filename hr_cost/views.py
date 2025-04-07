from datetime import date
from calendar import monthrange
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum

from hr_data.models import Employee
from .services import save_timesheet_to_csv, salary_calculation

from .models import WorkTime, Salary, Bonus, TimeSheet, UploadTimeSheet, TimeSheetAbsence
from .forms import WorkTimeForm, BonusForm

 # Получаем текущий месяц и год
today = timezone.now()
current_month = today.month
current_year = today.year

# Create your views here.
def index(request):
    return render(request, 'hr_cost/index.html')

def timesheet_download(request):
    ''' вывод загруженных из файла данных, которые будут загружать в таблицы табеля за текущий месяц'''
    # Получаем всех сотрудников
    employees = Employee.objects.all().order_by('last_name', 'first_name', 'middle_name')

    # Создаем список для хранения данных табеля
    timesheet_data = []

     # Генерация списка дат для текущего месяца    
    _, num_days = monthrange(current_year, current_month)
    dates = []
    for day in range(1, num_days + 1):
        current_date = date(current_year, current_month, day)
        weekday = current_date.weekday()  # Понедельник = 0, Воскресенье = 6
        dates.append({
            'date': f"{day:02d}",
            'weekday': weekday  # Добавляем информацию о дне недели
        })
    for employee in employees:
        # Получаем табель сотрудника для текущего месяца
        work_times =UploadTimeSheet.objects.filter(
            code=employee.code,
            date__month=current_month,
            date__year=current_year
        ).order_by('date')
        

        # Создаем словарь для хранения данных по дням
        employee_data = {
            'employee': f"{employee.last_name} {employee.first_name} {employee.middle_name}",
            'code': f"{employee.code}",
            'hours': [''] * num_days,  # Инициализируем список пустыми значениями
           
        }

        # Заполняем данные по дням
        for work_time in work_times:
            day = work_time.date.day - 1  # Индекс дня в списке
            employee_data['hours'][day] = str(work_time.timesheet_data)
        
        timesheet_data.append(employee_data)     
    

    return render(request, 'hr_cost/timesheet_download.html', {
        'timesheet_data': timesheet_data,
        'dates': dates,
        'current_month': today,
        'employees': employees,
       
    })

def timesheet_list(request):
    ''' вывод таблицы табеля за текущий месяц'''
    # Получаем всех сотрудников
    employees = Employee.objects.all().order_by('last_name', 'first_name', 'middle_name')

    # Создаем список для хранения данных табеля
    timesheet_data = []

     # Генерация списка дат для текущего месяца    
    _, num_days = monthrange(current_year, current_month)
    dates = []
    for day in range(1, num_days + 1):
        current_date = date(current_year, current_month, day)
        weekday = current_date.weekday()  # Понедельник = 0, Воскресенье = 6
        dates.append({
            'date': f"{day:02d}",
            'weekday': weekday  # Добавляем информацию о дне недели
        })
    for employee in employees:
        # Получаем табель сотрудника для текущего месяца
        work_times =TimeSheet.objects.filter(
            code=employee.code,
            date__month=current_month,
            date__year=current_year
        ).order_by('date')
        total_hours=WorkTime.objects.filter(code=employee.code).aggregate(summa=Sum('hours_worked'))
        total_hours=total_hours['summa']
        

        # Создаем словарь для хранения данных по дням
        employee_data = {
            'employee': f"{employee.last_name} {employee.first_name} {employee.middle_name}",
            'code': f"{employee.code}",
            'hours': [''] * num_days,  # Инициализируем список пустыми значениями
            'total_hours':total_hours #Сумма часов по сотруднику
           
        }

        # Заполняем данные по дням
        for work_time in work_times:
            day = work_time.date.day - 1  # Индекс дня в списке
            employee_data['hours'][day] = str(work_time.timesheet_data)
        
        timesheet_data.append(employee_data)
    
    # Сохраняем табель в CSV
    save_timesheet_to_csv(timesheet_data, dates, current_month, current_year)       
    

    return render(request, 'hr_cost/timesheet_list.html', {
        'timesheet_data': timesheet_data,
        'dates': dates,
        'current_month': today,
        'employees': employees,
       
    })

def timesheet(request):
    ''' вывод таблицы табеля за текущий месяц'''
   

    # Получаем всех сотрудников
    employees = Employee.objects.all().order_by('last_name', 'first_name', 'middle_name')

    # Создаем список для хранения данных табеля
    timesheet_data = []

    # Генерация списка дат для текущего месяца
    
    _, num_days = monthrange(current_year, current_month)
    dates = []
    for day in range(1, num_days + 1):
        current_date = date(current_year, current_month, day)
        weekday = current_date.weekday()  # Понедельник = 0, Воскресенье = 6
        dates.append({
            'date': f"{day:02d}",
            'weekday': weekday  # Добавляем информацию о дне недели
        })   
    
    # Обработка формы добавления отработанного времени
    if request.method == 'POST':
        form = WorkTimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timesheet')  # Перенаправляем на ту же страницу
    else:
        form = WorkTimeForm()

    for employee in employees:
        # Получаем отработанные часы для текущего месяца
        work_times = WorkTime.objects.filter(
            code=employee.code,
            date__month=current_month,
            date__year=current_year
        ).order_by('date')
        # total_hours=WorkTime.objects.filter(employee=employee).aggregate(summa=Sum('hours_worked'))
        # total_hours=total_hours['summa']
        total_hours = sum(int(work_time.hours_worked) for work_time in work_times)

        # Создаем словарь для хранения данных по дням
        employee_data = {
            'employee': f"{employee.last_name} {employee.first_name} {employee.middle_name}",
            'code': f"{employee.code}",
            'hours': [''] * num_days,  # Инициализируем список пустыми значениями
            # 'total_hours':total_hours['summa'] #Сумма часов по сотруднику
            'total_hours':total_hours #Сумма часов по сотруднику
        }
       

        # Заполняем данные по дням
        for work_time in work_times:
            day = work_time.date.day - 1  # Индекс дня в списке
            employee_data['hours'][day] = str(work_time.hours_worked)
            

        timesheet_data.append(employee_data)
    
    # Сохраняем табель в CSV
    save_timesheet_to_csv(timesheet_data, dates, current_month, current_year)    

    return render(request, 'hr_cost/timesheet_work.html', {
        'timesheet_data': timesheet_data,
        'dates': dates,
        'current_month': today,
        'form': form,  # Передаем форму в шаблон
    })

def timesheet_absence(request):
    ''' вывод таблицы табеля отсутствующих сотрудников'''

    # Получаем всех сотрудников
    employees = Employee.objects.all().order_by('last_name', 'first_name', 'middle_name')

    # Создаем список для хранения данных табеля
    timesheet_data = []

     # Генерация списка дат для текущего месяца    
    _, num_days = monthrange(current_year, current_month)
    dates = []
    for day in range(1, num_days + 1):
        current_date = date(current_year, current_month, day)
        weekday = current_date.weekday()  # Понедельник = 0, Воскресенье = 6
        dates.append({
            'date': f"{day:02d}",
            'weekday': weekday  # Добавляем информацию о дне недели
        })
    for employee in employees:
        # Получаем табель сотрудника для текущего месяца
        work_times = TimeSheetAbsence.objects.filter(
            code=employee.code,
            date__month=current_month,
            date__year=current_year
        ).order_by('date')
        total_hours=WorkTime.objects.filter(code=employee.code).aggregate(summa=Sum('hours_worked'))
        total_hours=total_hours['summa']
        

        # Создаем словарь для хранения данных по дням
        employee_data = {
            'employee': f"{employee.last_name} {employee.first_name} {employee.middle_name}",
            'code': f"{employee.code}",
            'hours': [''] * num_days,  # Инициализируем список пустыми значениями
            'total_hours':total_hours #Сумма часов по сотруднику
           
        }

        # Заполняем данные по дням
        for work_time in work_times:
            day = work_time.date.day - 1  # Индекс дня в списке
            employee_data['hours'][day] = str(work_time.timesheet_data)
        
        timesheet_data.append(employee_data)
    
    # Сохраняем табель в CSV
    save_timesheet_to_csv(timesheet_data, dates, current_month, current_year)       
    

    return render(request, 'hr_cost/timesheet_absebce.html', {
        'timesheet_data': timesheet_data,
        'dates': dates,
        'current_month': today,
        'employees': employees,
       
    })


def add_work_time(request):
    '''добавить отработанное время через форму'''
    if request.method == 'POST':
        form = WorkTimeForm(request.POST)
        employee = request.POST.get("employee")
        code = request.POST.get("code")
        dateform = request.POST.get("date")
        hours_worked = request.POST.get("hours_worked")
        TimeSheet.objects.create(
               code=code,
               employee = employee,
               date=dateform,
               timesheet_data=hours_worked
           )
        if form.is_valid():
            form.save()
            salary_calculation()
            return redirect('timesheet')
    else:
        form = WorkTimeForm()

    
    return render(request, 'hr_costform/add_work_time.html', {'form': form})


    

def add_bonus(request):
    '''добавить bonus через форму'''

    if request.method == 'POST':
        form = BonusForm(request.POST)
        employee = request.POST.get("employee")
        code = request.POST.get("code")
        bonus = request.POST.get("bonus")
        if form.is_valid():
            Bonus.objects.get_or_create(
                employee=employee,
                code= code,
                bonus=bonus,
                id=code
            )           
            salary_calculation()
            return redirect('add_bonus')
    else:
        form = BonusForm()

    bonus_list=Bonus.objects.all().order_by('employee')
   
    return render(request, 'hr_cost_forms/add_bonus.html', {'form': form, 'bonus_list':bonus_list, 'current_month':today })   

def bonus_delete(request, id):
    '''удалить бонус сотрудника из списка'''
    item=''
    try:
        item=Bonus.objects.get(id=id)
        print('bonus-delete item -',item)
        item.delete()
        print('Позиция - УДАЛЕНА')
        salary_calculation()
        return redirect('add_bonus') 
    except Exception as e:
        print(f'Позиция не удалена,{e}')    
    
    return render(request,  'hr_cost_forms/add_bonus.html',{'item':item}) 

   
def salary_list(request):
    '''вывод данных по зарплате за текущий месяц'''
    salary_employees=Salary.objects.all()
    last_date=timezone.now()
    if WorkTime.objects.all():
        last_date=WorkTime.objects.last().date
    # employee = (employee.employee for employee in salary_employees)
    return render(request, 'hr_cost/salary_list.html', {'items': salary_employees, 'current_date': last_date})
