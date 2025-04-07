from django.urls import path

from .views import (
    index,
    timesheet_download,
    timesheet_list,
    timesheet_absence,
    timesheet,
    add_work_time,
    add_bonus,
    bonus_delete,
    salary_list
)
from .views_upload import timesheet_upload, bonus_upload
from .services import (
    export_timesheet_csv,
    export_timesheet_pdf,
    salary_calculation,
    timesheet_save,
    export_salary_list_pdf
)

urlpatterns = [
    path("info", index, name="cost"),
    path("timesheet-download", timesheet_download, name="timesheet_download"),
    path("timesheet-list", timesheet_list, name="timesheet_list"),
    path("timesheet-absence", timesheet_absence, name="timesheet_absence"),
    path("timesheet", timesheet, name="timesheet"),
    path("add-work-time/", add_work_time, name="add_work_time"),
    path("export-timesheet-pdf/", export_timesheet_pdf, name="export_timesheet_pdf"),
    path("export-timesheet-csv/", export_timesheet_csv, name="export_timesheet_csv"),
    path("bonus-upload", bonus_upload, name="bonus_upload"),
    path("add-bonus", add_bonus, name="add_bonus"),
    path("bonus-delete/<int:id>", bonus_delete, name="bonus_delete"),
    path("salary-list", salary_list, name="salary_list"),
    path("salary_calculation", salary_calculation, name="salary_calculation"),
    path('export_salary_list_pdf', export_salary_list_pdf, name='export_salary_list_pdf'),
    path("timesheet_save", timesheet_save, name="timesheet_save"),
    path("timesheet_upload/", timesheet_upload, name="timesheet_upload"),
]
