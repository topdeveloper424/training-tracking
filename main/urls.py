
from django.urls import path,include
from . import views
from .forms import DirectoryForm,StepReq
app_name = 'main'

urlpatterns = [
    path('', views.index,name='index'),
    path('directory', views.directory,name='directory'),
    path('get-directory',views.get_directory,name='get_directory'),
    path('update-directory',views.update_directory,name='update_directory'),
    path('add-directory',views.add_directory,name='add_directory'),
    path('del-directory',views.del_directory,name='del_directory'),

    path('train-record', views.train_record,name='train_record'),
    path('add-record', views.add_record,name='add_record'),
    path('get-record', views.get_record,name='get_record'),
    path('del-record', views.del_record,name='del_record'),
    path('download-attach', views.download_attach,name='download_attach'),
    path('get-types', views.get_types,name='get_types'),


    path('step-req', views.step_req,name='step_req'),
    path('add-req', views.add_req,name='add_req'),
    path('del-req', views.del_req,name='del_req'),
    path('get-req', views.get_req,name='get_req'),
    path('update-req', views.update_req,name='update_req'),

]
