from django.db import models
# from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.models import User

class IDC(models.Model):
    """服务器机房位置信息"""
    name = models.CharField(max_length=64,unique=True)
    def __str__(self):
        return self.name

class HostUser(models.Model):
    """存储远程主机的用户信息 用于登录"""
    auth_type_choices = [(0,'ssh-password'),(1,'ssh-key')]
    auth_type = models.SmallIntegerField(choices=auth_type_choices)
    username = models.CharField(max_length=32)
    password = models.CharField(blank=True,null=True,max_length=128)

    class Meta:
        unique_together = ('username','password')

    def __str__(self):
        return "%s-%s" %(self.get_auth_type_display(),self.username)

class Host(models.Model):
    """服务器信息"""
    hostname = models.CharField(max_length=32,unique=True)
    ip_addr = models.CharField(max_length=32,unique=True)
    port = models.IntegerField(default=22)
    idc =models.ForeignKey('IDC',on_delete=models.CASCADE)

    def __str__(self):
        return "%s-%s" %(self.hostname,self.ip_addr)

class Token(models.Model):
    token = models.CharField(max_length=8,unique=True)
    expire = models.IntegerField(default=300)
    date = models.DateTimeField(auto_now_add=True)
    host_user_bind = models.ForeignKey('HostUserBind',on_delete=models.CASCADE)
    account = models.ForeignKey('Account',on_delete=models.CASCADE)

#==== 三表 堡垒机账户-
class HostGroup(models.Model):
    """web 运维等组的分类"""
    name = models.CharField(max_length=32,unique=True)
    group_bind_host = models.ManyToManyField('HostUserBind')

    def __str__(self):
        return self.name

class Account(models.Model):
    """
    堡垒机账户 -关联注册用户
            -关联 具体服务器ip
            -所属分组  如运维 HostGroup
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    bind_user_host = models.ManyToManyField("HostUserBind",blank=True)
    host_group = models.ManyToManyField("HostGroup",blank=True)

    def __str__(self):
        return str(self.user)

class HostUserBind(models.Model):
    """绑定主机和host的ip"""
    host = models.ForeignKey('Host',on_delete=models.CASCADE)
    host_user = models.ForeignKey('HostUser',on_delete=models.CASCADE)

    def __str__(self):
        return "%s-%s" %(self.host.hostname,self.host_user.username)

class Task(models.Model):
    task_type_choices = ((1,'cmd'),(2,'file_transfer'))
    task_type = models.SmallIntegerField(choices=task_type_choices)
    content= models.CharField('执行内容',max_length=256)
    date= models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey('Account',on_delete=models.CASCADE)
    timeout = models.IntegerField('超时时间',default=60)

class TaskLog(models.Model):
    status_choices = ((0,'成功'),(1,'失败'),(2,'超时'),(3,'初始化'))
    result= models.CharField(max_length=2048)
    date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=status_choices)
    host_user_bind = models.ForeignKey('HostUserBind',on_delete=models.CASCADE)
    task_id = models.ForeignKey('Task',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task_id','host_user_bind')