
from django import forms
from .models import SalaryHistory
class EmployeDepartmentForm(forms.Form):       
    '''form for select department's employees'''
    department_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите название отдела'}))  

class EmployeeSearchForm(forms.Form):
    '''form for searching an employee from the database'''
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'})
    )
MONTH_CHOICES =( 
    ("1", "Январь"), 
    ("2", "Февраль"), 
    ("3", "Март"), 
    ("4", "Апрель"), 
    ("5", "Май"),
    ("6", "Июнь"), 
    ("7", "Июль"), 
    ("8", "Август"), 
    ("9", "Сентябрь"), 
    ("10", "Октябрь"),
    ("11", "Ноябрь"),
    ("12", "Декабрь"), 
) 
class DateSalaryInput(forms.Form):
    # year=forms.IntegerField(widget=forms.NumberInput(), initial=2025)
    year=forms.IntegerField(initial=2025)
    month =forms.ChoiceField(choices = MONTH_CHOICES)  

