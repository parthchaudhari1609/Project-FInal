from django import forms
from .models import *
from bootstrap_datepicker_plus.widgets import DatePickerInput
from tempus_dominus.widgets import DatePicker


class ProjectCreationForm(forms.ModelForm):
    startDate = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    endDate = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Project
        fields = '__all__'
        
class ProjectTeamCreationForm(forms.ModelForm):
    class Meta:
        model = ProjectTeam
        fields = '__all__'

class ProjectModuleCreationForm(forms.ModelForm):
    # startDate = forms.DateField(widget=DatePicker())
    startDate = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    class Meta:
        model = ProjectModule
        fields = '__all__'
        # widgets = {
        #     'your_date_field': DatePickerInput(format='%d-%m-%Y')  
        # }
        

class ProjectStatusCreationForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'

class ProjectTaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class TaskAssignForm(forms.ModelForm):
    class Meta:
        model = UserTask
        fields = '__all__'