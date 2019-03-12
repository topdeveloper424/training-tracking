from django.template import  Context, loader,RequestContext
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Directory,TrainingRecord,StepReq
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings
from django.core.files import File
import datetime
# Create your views here.

def get_step_by_index(index):
    step = 0
    if index == 0:
        step = 0
    elif index == 1:
        step = 30
    elif index == 2:
        step = 60
    elif index == 3:
        step = 90
    elif index == 4:
        step = 120
    elif index == 5:
        step = 180
    elif index == 6:
        step = 270
    elif index == 7:
        step = 365
    elif index == 8:
        step = 'TOP'
    return step
        

def index(request):
    directories = Directory.objects.filter(status=True)
    res_list = []
    for directory in directories:
        empID = directory.EmpID
        title = directory.title
        req_list = {}
        res_row = {}
        res_row['EmpID'] = empID
        res_row['first_name'] = directory.first_name
        res_row['last_name'] = directory.last_name
        res_row['plant'] = directory.plant
        res_row['shift'] = directory.shift
        res_row['title'] = directory.title
        res_row['department'] = directory.department

        step_row = []
        step_row.append('N/A') #0  - 0
        step_row.append('N/A') #30  - 0
        step_row.append('N/A') #60  - 0
        step_row.append('N/A') #90  - 0
        step_row.append('N/A') #120  - 0
        step_row.append('N/A') #180  - 0
        step_row.append('N/A') #270  - 0
        step_row.append('N/A') #365  - 0
        step_row.append('N/A') #TOP  - 0

        date_row = []
        date_row.append('N/A') #0  - 0
        date_row.append('N/A') #30  - 1
        date_row.append('N/A') #60  - 2
        date_row.append('N/A') #90  - 3
        date_row.append('N/A') #120  - 4
        date_row.append('N/A') #180  - 5
        date_row.append('N/A') #270  - 6
        date_row.append('N/A') #365  - 7
        date_row.append('N/A') #TOP  - 8

        reqs = StepReq.objects.filter(title=title).order_by('step')
        for req in reqs:
            req_array = []
            if req.observation:
                req_array.append('O')
            if req.evaluation:
                req_array.append('E')
            if req.test:
                req_array.append('T')
            if req.status_change:
                req_array.append('S')
            req_len = len(req_array)


            records = TrainingRecord.objects.filter(EmpID = empID,title=title,eval_step=req.step)
            status_date = None
            fail_flag = False
            for rec in records:
                if rec.record_type == 'S':
                    status_date = rec.eval_date 
                if rec.grade:
                    for arr in req_array:
                        if arr ==  rec.record_type:
                            req_array.remove(arr)
                if rec.grade == False:
                    if rec.record_type in req_array:
                        fail_flag = True
            result = 'REQ'
            dat = None
            pass_count = 0
            if len(req_array) == 0:
                result = 'PASS'
                dat = status_date
                pass_count += 1
            elif fail_flag:
                result = 'FAIL'
            elif len(req_array) != req_len:
                result = 'PENDING'
            if req.step == '0':
                step_row[0] = result
                date_row[0] = dat
            elif req.step == '30':
                step_row[1] = result
                date_row[1] = dat
            elif req.step == '60':
                step_row[2] = result
                date_row[2] = dat
            elif req.step == '90':
                step_row[3] = result
                date_row[3] = dat
            elif req.step == '120':
                step_row[4] = result
                date_row[4] = dat
            elif req.step == '180':
                step_row[5] = result
                date_row[5] = dat
            elif req.step == '270':
                step_row[6] = result
                date_row[6] = dat
            elif req.step == '365':
                step_row[7] = result
                date_row[7] = dat
            elif req.step == 'TOP':
                step_row[8] = result
                date_row[8] = dat
            if pass_count == len(reqs):
                step_row[8] = 'PASS'
            elif fail_flag:
                step_row[8] = 'NOT ELIGIBLE'
            else:
                step_row[8] = 'ELIGIBLE'

        last_idx = -1
        for idx, val in enumerate(step_row):
            if val == 'PASS':
                last_idx = idx
        if last_idx != -1:
            for idx, val in enumerate(step_row):
                if idx <= last_idx or idx == len(step_row)-1:
                    continue
                if step_row[idx] == 'REQ':
                    cur_step = get_step_by_index(idx)
                    prev_step = get_step_by_index(last_idx)
                    last_date = date_row[last_idx]
                    diff = int(cur_step)  - int(prev_step)
                    last_date += datetime.timedelta(days=diff)
                    step_row[idx] = last_date
                    date_row[idx] = last_date
                    last_idx = idx
        for idx, val in enumerate(step_row):
            if step_row[idx] == None or step_row[idx] == 'REQ':
                step_row[idx] = 'N/A'
#            if step_row[idx] == 'REQ'
        res_row['steps'] = step_row
#        res_row['dates'] = date_row
        




                    




        res_list.append(res_row)
    print(res_list)
    return render(request, 'eval_schedule.html',{'res_list':res_list})

def directory(request):
    directories = Directory.objects.all()
    titles = StepReq.objects.values('title').distinct().order_by()
    return render(request,'directory.html',{'directories':directories,'titles':titles})

def get_directory(request):
    pk = request.GET['pk']
    directory = Directory.objects.filter(pk=pk)
    if directory:
        serialized_queryset = serializers.serialize('json', directory)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")

def add_directory(request):
    response = {}
    try:
        empID = request.GET['empID']
        first_name = request.GET['firstName']
        last_name = request.GET['lastName']
        plant = request.GET['plant']
        shift = int(request.GET['shift'])
        department = request.GET['department']
        title = request.GET['title']
        filters = Directory.objects.filter(title = title)
        if len(filters) > 0 and filters[0].status:
            response['status'] = 'error'
            return HttpResponse(json.dumps(response),content_type="application/json") 

        status = True
        if request.GET['status'] == 'false':
            status = False
        comment = request.GET['comment']
        directory = Directory(EmpID=empID,first_name=first_name,last_name=last_name,plant=plant,shift=shift,department=department,title=title,status=status,comment=comment)
        directory.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 


def del_directory(request):
    response = {}
    try:
        pk = request.GET['pk']
        Directory.objects.get(pk=pk).delete()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 



def update_directory(request):
    response = {}
    try:
        pk = request.GET['pk']
        empID = request.GET['empID']
        first_name = request.GET['firstName']
        last_name = request.GET['lastName']
        plant = request.GET['plant']
        shift = int(request.GET['shift'])
        department = request.GET['department']
        title = request.GET['title']
        status = True
        if request.GET['status'] == 'false':
            status = False
        comment = request.GET['comment']
        directory = Directory(pk=pk)
        directory.EmpID = empID
        directory.first_name = first_name
        directory.last_name = last_name
        directory.plant = plant
        directory.shift = shift
        directory.department = department
        directory.title = title
        directory.status = status
        directory.comment = comment
        directory.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 


def train_record(request):
    records = TrainingRecord.objects.order_by('title')
    emps = Directory.objects.values('EmpID').distinct().order_by()
    for emp in emps:
        directory = Directory.objects.filter(EmpID = emp['EmpID'])
        emp['title'] = directory[0].title
    return render(request,'train_record.html',{'records':records,'emps':emps})

@csrf_exempt
def add_record(request):
    saved = False
    if request.method == "POST":
        mode = int(request.POST['mode'])
        curPK = request.POST['curPK']
        empID = request.POST['editEmpID']
        step = request.POST['editStep']
        editType = request.POST['editType']
        editDate = request.POST['editDate']
        editGrade = request.POST['editGrade']
        editBy = request.POST['editBy']
        EmpID,title = empID.split("@@")
        print(EmpID)
        print(title)
        print(step)
        print(editType)
        print(editDate)
        grade = True
        if editGrade == 'F':
            grade = False
        print(editBy)
        if mode == 0:
            filters = TrainingRecord.objects.filter(EmpID=EmpID,title=title,eval_step=step,record_type=editType,grade=True)
            if len(filters) == 0:
                try:
                    attachment = request.FILES['editAttach']
                    record = TrainingRecord( EmpID=EmpID,title=title,eval_step=step,record_type=editType,eval_date=editDate,grade=grade,eval_by=editBy,attachment=request.FILES['editAttach'])
                    record.save()
                except Exception:
                    record = TrainingRecord( EmpID=EmpID,title=title,eval_step=step,record_type=editType,eval_date=editDate,grade=grade,eval_by=editBy)
                    record.save()


        elif mode == 1:
            record = TrainingRecord.objects.get(pk=curPK)
            record.EmpID = EmpID
            record.title = title
            record.eval_step = step
            record.record_type = editType
            record.eval_date = editDate
            record.grade = grade
            record.eval_by = editBy
            try:
                record.attachment = request.FILES['editAttach']
            except Exception:
                pass
            record.save()

    records = TrainingRecord.objects.order_by('EmpID')
    emps = Directory.objects.values('EmpID').distinct().order_by()
    for emp in emps:
        directory = Directory.objects.filter(EmpID = emp['EmpID'])
        emp['title'] = directory[0].title
    return render(request,'train_record.html',{'records':records,'emps':emps})


def get_record(request):
    try:
        pk = request.GET['pk']
        record = TrainingRecord.objects.filter(pk=pk)
        serialized_queryset = serializers.serialize('json', record)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    except Exception:
        return HttpResponse(json.dumps(""),content_type="application/json")

def del_record(request):
    response = {}
    try:
        pk = request.GET['pk']
        TrainingRecord.objects.get(pk=pk).delete()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 


def download_attach(request):
    response = {}
    pk = request.GET['pk']
    record = TrainingRecord.objects.filter(pk=pk)
    serialized_queryset = serializers.serialize('json', record)
    return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")

def get_types(request):
    response = {}
    try:
        empID = request.GET['editEmpID']
        EmpID,title = empID.split("@@")
        reqs = StepReq.objects.filter(title= title).order_by('step')
        serialized_queryset = serializers.serialize('json', reqs)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    except Exception:
        return HttpResponse(json.dumps(""),content_type="application/json") 


def step_req(request):
    reqs = StepReq.objects.values('title').distinct().order_by()
    count = 0
    for req in reqs:
        filters = StepReq.objects.filter(title=req['title']).order_by()
        count += 1
        steps = ""
        for f in filters:
            steps += f.step + ", "
        steps = steps[0:len(steps)-2]
        req['steps'] = steps
        req['count'] = count
    print(reqs)

    return render(request,'step_req.html',{'reqs':reqs})

def add_req(request):
    response = {}
    try:
        title = request.GET['title']
        reqs = request.GET['req']
        reqsJSON = json.loads(reqs)
        fitlers = StepReq.objects.filter(title = title)
        if len(fitlers) > 0:
            response['status'] = 'error'
            return HttpResponse(json.dumps(response),content_type="application/json") 
        for req in reqsJSON:
            observation = True
            if req['observation'] == 'N':
                observation = False
            evaluation = True
            if req['evaluation'] == 'N':
                evaluation = False
            test = True
            if req['test'] == 'N':
                test = False
            status_change = True
            if req['status'] == 'N':
                status_change = False
            

            req_new = StepReq(title = title,step=req['step'],observation = observation, evaluation = evaluation, test=test, status_change= status_change)
            req_new.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 

def del_req(request):
    response = {}
    try:
        title  = request.GET['title']
        StepReq.objects.filter(title = title).delete()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 

def get_req(request):
    title = request.GET['title']
    reqs = StepReq.objects.filter(title = title)
    if len(reqs) > 0:
        serialized_queryset = serializers.serialize('json', reqs)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")


def update_req(request):
    response = {}
    try:
        old_title = request.GET['oldTitle']
        title = request.GET['title']
        reqs = request.GET['req']
        reqsJSON = json.loads(reqs)
        StepReq.objects.filter(title = old_title).delete()
        for req in reqsJSON:
            observation = True
            if req['observation'] == 'N':
                observation = False
            evaluation = True
            if req['evaluation'] == 'N':
                evaluation = False
            test = True
            if req['test'] == 'N':
                test = False
            status_change = True
            if req['status'] == 'N':
                status_change = False

            req_new = StepReq(title = title,step=req['step'],observation = observation, evaluation = evaluation, test=test, status_change= status_change)
            req_new.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 







