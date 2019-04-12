# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
# from django.utils.safestring import mark_safe
# from django.db.models import F
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from audit import models
import random,string,datetime
from django.conf import settings
import json,os
from audit import taskhandler
from django.views.decorators.csrf import csrf_exempt
import zipfile
# from django.views import View

def send_zipfile(request,task_id,file_path):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    zip_file_name = 'task_id_%s_files' % task_id
    archive = zipfile.ZipFile(zip_file_name , 'w', zipfile.ZIP_DEFLATED)
    file_list = os.listdir(file_path)
    for filename in file_list:
        archive.write('%s/%s' %(file_path,filename),arcname=filename)
    archive.close()


def my_login(request):
    error = 'wrong name or password'
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd =  request.POST.get('password')
        obj=authenticate(username=user,password=pwd)
        if obj:
            login(request,obj)
            return redirect('/')

        return render(request,'login.html',{'error':error})


@login_required(login_url='/login')
def index(request):
    obj = models.Account.objects.filter(user=request.user.pk).first().bind_user_host.all()
    return render(request,'index.html',locals())



def host_list(request):
    global obj
    obj = models.Account.objects.filter(user=request.user.pk).first()
    return render(request,'host_list.html',{'obj':obj})



def ajax_host(request):
    '''
    ajax请求获取主机列表
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    if id:
        if id == '-1':
            host_list = obj.bind_user_host.all()
            print(host_list)
        else:
            host_list = models.Account.objects.filter(user=request.user.pk).first().host_group.get(id=id).group_bind_host.all()
        data = json.dumps(list(host_list.values_list('host__hostname','host__ip_addr','host__idc__name','host__port','host_user__username','host_id')),ensure_ascii=False)
        return HttpResponse(data)
    else:
        return HttpResponse('主机组不存在')

@login_required(login_url='/login')
def ajax_token(request):
    """
    生成token,用于shellinabox,浏览器模拟登录shell
    :param request:
    :return:
    """
    ex_time = datetime.datetime.now()-datetime.timedelta(models.Token.objects.filter(account=request.user.account).first().expire)
    host_id = request.POST.get('ip_id')
    token_obj = models.Token.objects.filter(account=request.user.account.id,date__lt=ex_time,host_user_bind__host=host_id).first()
    if token_obj:
        token = token_obj.token
    else:
        token = ''.join(random.sample(string.ascii_lowercase+string.digits,8))
        models.Token.objects.create(
            host_id=host_id,
            account=request.user.account,
            token=token
        )

    return JsonResponse({'token':token,'ip_id':host_id})


@login_required(login_url='/login')
def multi_cmd(request):
    """命令输入界面"""
    return render(request,'multi_cmd.html',{'obj':request.user.account})


@login_required(login_url='/login')
def multi_task(request):
    """批量执行命令,cmd/上传/下载文件"""
    task = taskhandler.Task(request)
    if task.is_valid():
        task_obj = task.run()
        return JsonResponse({'task_id':task_obj.id,'time_out':task_obj.timeout})
    return JsonResponse(task.errors,safe=False)


@login_required(login_url='/login')
def multi_files_transfer(request):
    random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
    return render(request,'multi_files_transfer.html',locals())  #文件上传下载页面


def task_file_download(request):
    task_id = request.GET.get('task_id')
    task_file_path = "%s/%s" % (settings.FILE_DOWNLOADS, task_id)
    return send_zipfile(request, task_id, task_file_path)


@login_required(login_url='/login')
def task_result(request):
    task_id = request.POST.get('task_id')
    results = list(models.TaskLog.objects.filter(task_id=task_id).values())
    return HttpResponse(json.dumps(results))


@login_required(login_url='/login')
@csrf_exempt    #使用第三方组件，没法携带crsf_token
def task_file_upload(request):
    file_obj = request.FILES.get('file')
    upload_path = '{base_path}/{personal_file}/{random_str}'.format(**{'base_path':settings.UPLOAD_FILE,'personal_file':request.user.account.id,'random_str':request.GET.get('random_str')})
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    with open('%s/%s' %(upload_path,file_obj.name),'wb+') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return HttpResponse(json.dumps({'msg':'上传成功','status':0}))



