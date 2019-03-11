from django.db import models
from django.utils.encoding import smart_text

# Create your models here.
from datetime import date

class Directory(models.Model):
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


    EmpID = models.CharField(max_length = 100, unique=True, default='')
    first_name = models.CharField(max_length=50,null=False,default='')
    last_name = models.CharField(max_length=50,null=False,default='')
    plant = models.CharField(max_length=4,choices = PLANT_CHOICE, default = NORTH)
    shift = models.IntegerField(null=False,default=1)
    department = models.CharField(max_length=4,choices = DEPARTMENT_CHOICE, default = PRODUCTION)
    title = models.CharField(max_length=200,null=False,default='')
    status = models.BooleanField(default=True)      # true: Active,  false: Closed
    comment = models.CharField(max_length=250)

    def __unicode__(self):
        return smart_text(self.first_name)

class TrainingRecord(models.Model):
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

    EmpID = models.CharField(max_length = 100, null=False, default='')
    title = models.CharField(max_length=200,null=False,default='')
    eval_step = models.CharField(max_length=20,null=False,default='0')
    record_type = models.CharField(max_length=100, choices = TYPE_CHOICE, default = TEST)
    eval_date = models.DateField(default=date.today)
    grade = models.BooleanField(default=True)       # true: PASS,  false: FAIL
    eval_by = models.CharField(max_length=150,null=False,default='')
    attachment = models.FileField(upload_to='attachments/%Y/%m/%d/')

    def get_emp_info(self):
        directory = Directory.objects.get(EmpID = self.EmpID)
        return directory

class StepReq(models.Model):
    title = models.CharField(max_length=200,null=False,default='')
    step = models.CharField(max_length=20,null=False,default='0')
    observation = models.BooleanField(default=True)         #true: Y,  false: N
    evaluation = models.BooleanField(default=True)
    test = models.BooleanField(default=True)
    status_change = models.BooleanField(default=True)



    

