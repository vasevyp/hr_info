from django.urls import path

from .views import (
    index,
    main,
    DepartmentList,
    employee_list,
    employee_detail,
    export_employee_list_pdf,
    employee_search,
    history_salary,
    history_timesheet,
    timesheet_select,
    salary_select,
    main_history_select,
    employee_vacation_list
)

urlpatterns = [
    path("", index, name="index"),
    path("main", main, name="main"),
    path("department-list", DepartmentList.as_view(), name="department_list"),
    path("employee-list", employee_list, name="employee_list"),
    path("employees/<int:pk>/", employee_detail, name="employee_detail"),
    path(
        "export-employee-list-pdf/",
        export_employee_list_pdf,
        name="export_employee_list_pdf",
    ),
    path("employee-search/", employee_search, name="employee_search"),
    path("history-salary", history_salary, name="history_salary"),
    path("history-timesheet", history_timesheet, name="history_timesheet"),
    path("timesheet_select", timesheet_select, name="timesheet_select"),
    path("salary_select", salary_select, name="salary_select"),
    path("main_history_select", main_history_select, name="main_history_select"),
    path('employee-vacation-list', employee_vacation_list, name="employee_vacation_list")
]
