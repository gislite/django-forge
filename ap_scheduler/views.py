from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events

print('django-apscheduler')


def job2(name):
    # 具体要执行的代码
    print('{} 任务运行成功！{}'.format(name, time.strftime("%Y-%m-%d %H:%M:%S")))


def job3(name):
    print('{} 任务运行成功！{}'.format(name, time.strftime("%Y-%m-%d %H:%M:%S")))


def job4(name):
    print('{} 任务运行成功！{}'.format(name, time.strftime("%Y-%m-%d %H:%M:%S")))


# 实例化调度器
scheduler = BackgroundScheduler(timezone='Asia/Shanghai') # 这个地方要加上时间，不然他有时间的警告

# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")


# 添加任务1
# 每隔5s执行这个任务，这个就是装饰器的玩法
@register_job(scheduler, "interval", seconds=5, args=['老K'], id='job1', replace_existing=True)
def job1(name):
    # 具体要执行的代码
    print('{} 任务运行成功！{}'.format(name, time.strftime("%Y-%m-%d %H:%M:%S")))


def index(request):


    # 下面这就是add_job的方式 interval
    scheduler.add_job(job2, "interval", seconds=10, args=['老Y'], id="job2", replace_existing=True)

    # 下面这就是add_job的方式 crontab  16点 38分  40分执行
    scheduler.add_job(job3, 'cron', hour='16', minute='38,40', args=['鬼人'], id='job3', replace_existing=True)


    # 固定时间运行
    # @register_job(scheduler, 'date', id='test', run_date='2019-07-07 22:49:00')
    scheduler.add_job(job4, 'date', args = ['bk'], id='job4', run_date='2023-07-07 22:49:00')

    """
    20220408更新 
    id可以不加,如果不加ID是这个应用view下的函数名字

    replace_existing=True 这个东西不加的话，他会提示ID冲突了,我查了好多文章，把这答案找出来了 。
    """
    # 监控任务
    register_events(scheduler)  # 这个event 这个会有已经被废弃的用法删除线，我不知道这个删除了 ，还会不会好用
    # 调度器开始运行
    scheduler.start()
    return HttpResponse('ok')

