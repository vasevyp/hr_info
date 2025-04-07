from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import WorkTime, Salary, Bonus, UploadTimeSheet, TimeSheet, TimeSheetAbsence



@admin.register(UploadTimeSheet)
class UploadTimeSheetAdmin(ImportExportModelAdmin):
    list_display = ('employee', 'code', 'date', 'timesheet_data')
    # search_fields = ('employee', 'date')
    list_filter = ('employee', 'date')

@admin.register(TimeSheet)
class TimeSheetAdmin(ImportExportModelAdmin):
    list_display = ('employee', 'code', 'date', 'timesheet_data')
    search_fields = ('employee', 'date')
    list_filter = ('employee', 'date')
    save_on_top = True


@admin.register(WorkTime)
class WorkTimeAdmin(ImportExportModelAdmin):
    list_display = ('employee', 'code', 'date', 'hours_worked')
    search_fields = ('employee', 'date')
    list_filter = ('employee', 'date')
    save_on_top = True
@admin.register(TimeSheetAbsence)
class TimeSheetAbsenceAdmin(ImportExportModelAdmin):
    list_display = ('employee', 'code', 'date', 'timesheet_data')
    search_fields = ('employee', 'date')
    list_filter = ('employee', 'date')
    save_on_top = True    

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'accrued_salary', 'bonus', 'salary') 
    list_filter = ('employee',)   

@admin.register(Bonus)
class BonusAdmin(ImportExportModelAdmin):
    list_display = ('employee', 'id', 'code', 'bonus') 
    list_filter = ('employee',)   
