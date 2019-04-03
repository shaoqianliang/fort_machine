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
# from django.views import View



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
    #必须变成models下的类才有属性,queryset只是个特殊的字典
    return render(request,'index.html',locals())



def register(request):
    """
    暂时不提供注册
    :param request:
    :return:
    """
    pass


def host_list(request):
    global obj
    obj = models.Account.objects.filter(user=request.user.pk).first()
    return render(request,'host_list.html',{'obj':obj})



def ajax_host(request):
    #获取我的主机列表
    # //get 等价于filter（）.first（）
    id = request.POST.get('id')
    if id:
        if id == '-1':
            host_list = obj.bind_user_host.all()
            print(host_list)
        else:
            host_list = models.Account.objects.filter(user=request.user.pk).first().host_group.get(id=id).group_bind_host.all()
        data = json.dumps(list(host_list.values_list('host__hostname','host__ip_addr','host__idc__name','host__port','host_user__username','host_id')),ensure_ascii=False)
    return HttpResponse(data)

@login_required(login_url='/login')
def ajax_token(request):
    #拿到过时时间
    ex_time = datetime.datetime.now()-datetime.timedelta(models.Token.objects.filter(account=request.user.account).first().expire)
    # 生成8位随机验证码,sample:可迭代对象中取k个值
    host_id = request.POST.get('ip_id')
    token_obj = models.Token.objects.filter(account=request.user.account.id,date__lt=ex_time,host_user_bind__host=host_id).first()
    if token_obj:
        token = token_obj.token
    else:
        token = ''.join(random.sample(string.ascii_lowercase+string.digits,8))
        #？？？疑问点 外键关联或者.属性，不然携带_id(oneToone)
        models.Token.objects.create(
            host_id=host_id,
            account=request.user.account,
            token=token
        )

    return JsonResponse({'token':token,'ip_id':host_id})


    #all()或者models.User.objects() values value__list 都是queryset对象，看做特殊的列表，内部是字典
    #first（）则是Model的子类，通过属性.查找

@login_required(login_url='/login')
def multi_cmd(request):
    """命令输入界面"""
    return render(request,'multi_cmd.html',{'obj':request.user.account})


@login_required(login_url='/login')
def multi_task(request):
    """批量执行命令"""
    task = taskhandler.Task(request)   #验证用后，执行cmd或上传
    if task.is_valid():
        task_obj = task.run()
        return JsonResponse({'task_id':task_obj.id,'time_out':task_obj.timeout})
    return JsonResponse(task.errors,safe=False)


@login_required(login_url='/login')
def multi_files_transfer(request):
    random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
    return render(request,'multi_files_transfer.html',locals())  #文件上传下载页面


def task_file_download(request):
    pass


@login_required(login_url='/login')
def task_result(request):
    task_id = request.POST.get('task_id')
    results = list(models.TaskLog.objects.filter(task_id=task_id).values())
    return HttpResponse(json.dumps(results))


@login_required(login_url='/login')
@csrf_exempt    #使用第三方组件，没法携带crsf_token
def task_file_upload(request): #//客户端到堡垒机，临时下载
    file_obj = request.FILES.get('file')
    upload_path = '{base_path}/{personal_file}/{random_str}'.format(**{'base_path':settings.UPLOAD_FILE,'personal_file':request.user.account.id,'random_str':request.GET.get('random_str')})
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    with open('%s/%s' %(upload_path,file_obj.name),'wb+') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return HttpResponse(json.dumps({'msg':'上传成功','status':0}))



