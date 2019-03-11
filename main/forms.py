from django import forms
from django.forms import ModelForm
from .models import Directory,TrainingRecord, StepReq

class DirectoryForm(ModelForm):
    class Meta:
        NORTH = 'N'
        SOUTH = 'S'
        VINE = 'V'
        OVERLAND = 'O'
        PLANT_CHOICE = (
            (NORTH, 'North'),
            (SOUTH,'South'),
            (VINE,'Vine'),
            (OVERLAND,'Overland'),
        )

        PRODUCTION = 'P'
        QUALITY = 'Q'
        SANITATION = 'S'
        WAREHOUSE='W'
        ADMIN='A'

        DEPARTMENT_CHOICE = (
            (PRODUCTION,'Production'),
            (QUALITY,'Quality'),
            (SANITATION,'Sanitation'),
            (WAREHOUSE,'Warehouse'),
            (ADMIN,'Admin'),
        )

        STATUS_CHOICE = (
            (True,'Active'),
            (False,'Closed'),
        )


        model = Directory

        fields = ['EmpID','first_name','last_name','plant','shift','department','title','status','comment']

        widgets = {
            'EmpID': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type Emp ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type Last Name'}),
            'plant': forms.Select(attrs={'class': 'form-control','placeholder':'Please Select Plant'},choices=PLANT_CHOICE),
            'shift': forms.TextInput(attrs={'type':'number','class': 'form-control','placeholder':'Please type shift'}),
            'department': forms.Select(attrs={'class': 'form-control','placeholder':'Please Select department'},choices=DEPARTMENT_CHOICE),
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type title'}),
            'status': forms.Select(attrs={'class': 'form-control','placeholder':'Please select status'},choices=STATUS_CHOICE),
            'comment': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type comment'}),
        }

class TrainingForm(ModelForm):
    class Meta:
        OBSERVATION = 'O'
        EVALUATION = 'E'
        TEST='T'
        STATUS_CHANGE='S'
        TYPE_CHOICE = (
            (OBSERVATION,'Observation'),
            (EVALUATION,'Evaluation'),
            (TEST,'Test'),
            (STATUS_CHANGE,'Status Change'),
        )
        model = TrainingRecord
        fields = ['EmpID','title','eval_step','record_type','eval_date','grade','eval_by','attachment']
    
        widgets = {
            'EmpID': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StepReqForm(ModelForm):
    class Meta:
        STATUS_CHOICE = (
            (True,'Yes'),
            (False,'No'),
        )

        model = StepReq

        fields = ['title','step','observation','evaluation','test','status_change']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type title'}),
            'step': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type step'}),
            'observation': forms.Select(attrs={'class': 'form-control','placeholder':'Please type observation'},choices=STATUS_CHOICE),
            'evaluation': forms.Select(attrs={'class': 'form-control','placeholder':'Please type evaluation'},choices=STATUS_CHOICE),
            'test': forms.Select(attrs={'class': 'form-control','placeholder':'Please type test'},choices=STATUS_CHOICE),
            'status_change': forms.Select(attrs={'class': 'form-control','placeholder':'Please type status_change'},choices=STATUS_CHOICE),

        }


        