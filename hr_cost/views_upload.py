''' для загрузки данных из файлов .xlsx'''
import sqlite3
import openpyxl
import pandas as pd

from django.shortcuts import render

from .services import salary_calculation
from .models import UploadTimeSheet, Bonus


def timesheet_upload(request):
    ''' Загрузка табеля из xlsx file with pandas'''
    print('start timesheet_loading()')
    UploadTimeSheet.objects.all().delete()
    print('delete old UploadTimeSheet objects from DB')
    try:
        if request.method == 'POST' and request.FILES['myfile']:
          
            myfile = request.FILES['myfile']
           
            wookbook = openpyxl.load_workbook(myfile)
            worksheet = wookbook.active
            print(worksheet)
            data = worksheet.values
            # Get the first line in file as a header line
            columns = next(data)[0:]
            df = pd.DataFrame(data, columns=columns)
            df['id']=df['code']
            print('dataframe==\n',df,'\ntype data:',type(df))
            print(df.code,df.employee)
            conn = sqlite3.connect('db.sqlite3')
            print('conn--',conn)
            df.to_sql('hr_cost_uploadtimesheet',
                                conn, if_exists='replace') #таблица для данных
            data=UploadTimeSheet.objects.all()         

            return render(request, 'hr_cost_upload/timesheet_upload.html', {'myfile': myfile, 'datas':data,})
    except TypeError as identifier:
        print('Exception as identifier=', identifier)
        return render(request, 'hr_cost_upload/timesheet_upload.html', {'item_except': identifier})

    return render(request, 'hr_cost_upload/timesheet_upload.html', {})


def bonus_upload(request):
    '''Загрузка бонуса из xlsx file with pandas'''
    print('start bonus_loading()')
    Bonus.objects.all().delete()
    print('delete objects DB')
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            print('if POST -OK')#+
            myfile = request.FILES['myfile']
            print('myfile==',myfile)#+
            wookbook = openpyxl.load_workbook(myfile)
            worksheet = wookbook.active
            print(worksheet)
            data = worksheet.values
            # Get the first line in file as a header line
            columns = next(data)[0:]
            df = pd.DataFrame(data, columns=columns)
            df['id']=df['code']
            print('dataframe==\n',df,'\ntype data:',type(df))
            print(df.code,df.employee)
            conn = sqlite3.connect('db.sqlite3')
            print('conn--',conn)
            df.to_sql('hr_cost_bonus',
                                conn, if_exists='replace') #таблица для данных
            
            salary_calculation()
            data=Bonus.objects.all()         

            return render(request, 'hr_cost_upload/bonus_upload.html', {'myfile': myfile, 'datas':data,})
    except TypeError as identifier:
        print('Exception as identifier=', identifier)
        return render(request, 'hr_cost_upload/bonus_upload.html', {'item_except': identifier})

    return render(request, 'hr_cost_upload/bonus_upload.html', {})
