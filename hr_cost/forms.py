"""forms for employee data"""

from django import forms

from hr_data.models import Employee
from . models import WorkTime, Bonus



class WorkTimeForm(forms.ModelForm):
    """form for recording employees' working hours"""
    class Meta:
        """admin for working hours"""
        model = WorkTime
        fields = ["employee", "code", "date", "hours_worked"]
        
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "hours_worked": forms.TextInput(
                attrs={"placeholder": "Введите отработанные часы"}
            ),
        }


class BonusForm(forms.ModelForm):
    """form for recording employees' bonus"""

    class Meta:
        """admin for working hours"""

        model = Bonus
        fields = ["code", "employee", "bonus"]
       
        widgets = {
            
            "bonus": forms.TextInput(attrs={"placeholder": "Введите бонус в руб."}),
        }


