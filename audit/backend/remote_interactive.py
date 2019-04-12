import datetime
import paramiko
import os,sys

def cmd(task_log):
    """基于sshclient登录"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #申明不需要在记录中

        ssh.connect(task_log.host_user_bind.host.ip_addr,
                    task_log.host_user_bind.host.port,
                    task_log.host_user_bind.host_user.username,
                    task_log.host_user_bind.host_user.password,
                    timeout=15)
        stdin,stdout,stderr = ssh.exec_command(task_log.task_id.content)  #执行任务
        result =stdout.read() + stderr.read()
        ssh.close()
        task_log.result = result or 'run cmd has no result'
        task_log.status = 0
        task_log.save()
    except Exception as e:
        print({'error':e})

def file_transfer(task_log):
    import django
    django.setup()
    from django.conf import settings
    from audit import models
    task_data = json.loads(task_obj.task_id.content)
    models.TaskLog.objects.filter(id=task_log.id).update(result='图片保存到服务器')
    ssh = paramiko.Transport((task_log.host_user_bind.host.ip_addr,
                              task_log.host_user_bind.host.port))
    ssh.connect(username=task_log.host_user_bind.host_user.username,password=task_log.host_user_bind.host_user.password)
    sftp = paramiko.SFTPClient.from_transport(ssh) #通过ssh通道传输
    if task_data['file_transfer'] == 'send':
        upload_dir = '%s/%s/%s' %( settings.UPLOAD_FILE,
                                  task_obj.task_id.account.id,
                                   task_data.get('random_str'))
        for file_name in os.listdir(upload_dir): #//获取目录下的所有文件或文件夹
            sftp.put('%s/%s' %(upload_dir,file_name), '%s/%s'%(task_data.get('remote_path'), file_name))
        task_obj.result = "Done!send files successful"
    else:
        download_dir = "%s/%s" %(settings.FILE_DOWNLOADS,task_obj.task_id)
        if os.path.exists(download_dir):
            os.makedirs(download_dir,exist_ok=True)  #//允许存在，不然报错
            remote_filename = os.path.basename(task_data.get('remote_path'))
            local_file_path = "%s/%s.%s" % (download_dir, task_obj.host_user_bind.host.ip_addr, remote_filename) #生成唯一路径
            sftp.get(remote_filename,local_file_path)
            task_obj.result = "Download %s from %s" %(local_file_path,remote_filename)


if __name__ == "__main__":
    bash_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(bash_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fort_machine.settings")
    import django
    django.setup()
    from audit import models
    import json
    task_id = sys.argv[1]
    import multiprocessing
    pool = multiprocessing.Pool(processes=10)
    task_obj = models.Task.objects.filter(id=task_id).first()
    if task_obj.task_type == 1:
        func = cmd
    else:
        func = file_transfer
    for task_log in task_obj.tasklog_set.all():
        pool.apply_async(func,args=task_log)
    pool.join()
    pool.close()