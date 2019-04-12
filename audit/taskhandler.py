from fort_machine import settings
from audit import models
import json
from django.db.transaction import atomic #事务操作
class Task():
    """
    is_valid:验证任务类型
    file__transfer:执行文件上传/下载
    cmd:堡垒机获取服务器资源
    task_data:{'task_type':'cmd':'selected_id_host':[.....],'content':'执行的内容或命令'}
    """
    def __init__(self,request):
        self.request = request
        self.errors = []
        self.task_data = None #task_data

    def is_valid(self): #验证提交的命令
        self.task_data = json.loads(self.request.POST.get('task_data')) #json
        if self.task_data['task_type'] == 'cmd' and self.task_data.get('selected_host_ids'):
            return  True
        elif self.task_data['task_type'] == 'file_transfer':
            return True
        else:
            self.errors.append({'msg':'cmd or host is empty or wrong,please sure it successful'})
            return False

    def file_transfer(self):
        pass

    def cmd(self):   #创建任务id，日志，防止等待，开启进程执行任务脚本
        import subprocess
        multi_task_obj = subprocess.Popen('python3 %s %s' %(settings.MULTI_TASK_SCRIPT,self.task_data),shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)    #开启多进程，远程连接服务器，分步执行命令,适合传递单个简单参数
        result = multi_task_obj.stdout.read()+multi_task_obj.stderr.read()
        print(result.decode('utf-8'))

    @atomic
    def run(self):
        """创建任务id,cmd
        和文件传输只是type有区别"""
        if self.task_data['task_type'] == 'cmd':
            type_choice = 1
            content = self.task_data.get('cmd')
        else:
            type_choice = 0
            content = self.request.POST.get('task_data')
        # task_obj = models.Task.objects.create(task_type=type_choice,account=self.request.user.account,content=self.task_data['content'])
        # host_lists = self.task_data.get('selected_host_ids')
        task_obj = models.Task.objects.create(task_type=type_choice, account=self.request.user.account,content=content)
        host_lists = self.task_data.get('selected_host_ids')
        task_list = []
        for host_id in set(host_lists):  #ip提交有重复
            task_list.append(models.TaskLog(task_id_id=task_obj.id,host_user_bind_id=host_id,status=3))  #实例化数据对象,fk等字段加_id
        models.TaskLog.objects.bulk_create(task_list,100)  #批量创建任务日志
        # getattr(self,self.task_data['task_type'])() #执行cmd或者文件传输
        import subprocess
        multi_task_obj = subprocess.Popen('python3 %s %s' %(
                        settings.MULTI_TASK_SCRIPT,
                        task_obj.id), shell=True,
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        return task_obj