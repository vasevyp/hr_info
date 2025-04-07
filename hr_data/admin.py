from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import Department, Vacation, Employee, SalaryHistory, TimeSheetHistory


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'code', 'manager_job_title', 'manager_last_name','manager_first_name', 'manager_middle_name')

class VacationInline(admin.TabularInline):
    model = Vacation
    extra = 1
    fields = ['planned_start_date', 'planned_end_date', 'actual_start_date', 
              'actual_end_date', 'planned_days', 'remaining_days']
    readonly_fields = ['remaining_days']

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = (
        'code', 'first_name', 'last_name', 'department', 'position', 'hire_date', 'contract_expiration'
    )
    inlines = [VacationInline]
    search_fields = ('code', 'first_name', 'last_name', 'department__name')
    list_filter = ('department__name', 'gender', 'civil_status')
    save_on_top = True
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('code', 'first_name', 'middle_name', 'last_name', 'gender', 'birthday', 'place_of_birth')
        }),
        ('Паспортные данные и адреса', {
            'fields': ('passport', 'address', 'provincial_address')
        }),
        ('Контактная информация', {
            'fields': ('phone',)
        }),
        ('Гражданство и статус', {
            'fields': ('citizenship', 'civil_status')
        }),
        ('Профессиональная информация', {
            'fields': ('department', 'profession', 'position', 'hire_date', 'contract_expiration', 'salary_rate',  'salary_type')
        }),
        ('Дополнительная информация', {
            'fields': ('remarks',)
        }),
        ('Системные данные', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_date', 'updated_date')

@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'code', 'planned_start_date', 'planned_end_date', 
                    'actual_start_date', 'actual_end_date', 'planned_days', 'remaining_days']
    list_filter = ['employee', 'planned_start_date']
    search_fields = ['employee__full_name', 'employee__employee_code']
    date_hierarchy = 'planned_start_date'

@admin.register(SalaryHistory)
class SalaryHistoryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'period', 'accrued_salary', 'bonus', 'salary') 
    list_filter = ('employee', 'period') 
    save_on_top = True

@admin.register(TimeSheetHistory)
class TimeSheetHistoryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'period', 'date', 'timesheet_data') 
    list_filter = ('employee', 'date')  
    save_on_top = True   