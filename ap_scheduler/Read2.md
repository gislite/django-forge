Django使用django-apscheduler的问题
发布于2021-10-26 10:35:30阅读 9730
Django定时任务
由于业务需要，后台要有一个定时任务的功能，起初考虑单独出来使用Linux系统的corn来实现。但是考虑到这样会很不方便。于是便寻找定时任务的模块，就找到了APScheduler，考虑到要在Django中使用，后来就采用了django-apscheduler来作为定时任务的模块，但是这个模块本身有bug。当你使用uwsgi部署并开启多进程的时候，该模块的内置使用get方法来获取任务列表，然后就会报错。因为同一时间有了多个任务，get方法获取到多个任务的时候就会抛出异常。
 Django定时任务不要使用django-apscheduler模块，直接使用APScheduler模块即可。

APScheduler官方使用指南，在这份指南中明确指出django-apscheduler并不是官方支持的。

使用APScheduler
现在，我们避免了django-apscheduler模块抛出异常问题，但是我们还有一个问题等待解决，那就是uWsgi使用多进程模式启动Django项目，因此我们会有多个进程去执行这个定时任务，导致定时任务被重复执行。解决这个问题的方法，我们直接就会想到采用加锁的方式。第一个拿到锁的进程，执行定时任务，其余的进程由于拿不到锁，因此也就不会执行定时任务。下面给出两种加锁方案，分别适用于不同的场合。

Redis分布式锁
redis中放置锁，是可以解决分布式下的问题。当然，如果你没有使用分布式，也是可以使用redis锁的。

def testaps():
    cache=get_redis_connection("default")
    key = f"APS_Lock"
    lock = cache.set(key, value=1, nx=True, ex=180)     # 180s之后锁自动消失，因此无需释放锁。
    if lock:
        scheduler = BackgroundScheduler()
        def my_job():
            print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        scheduler.add_job(my_job, 'interval', seconds=10)
        scheduler.start()
    else:
        ...
testaps()   # 执行函数
复制
当多个进程都执行testaps方法的时候，只有第一个拿到redis锁（这是个原子操作）的进程才能开启定时任务，其他的进程都无法开启定时任务，这样就可以保证定时任务只被执行一次。

文件锁
在不是分布式的场景下（或者没有redis这种工具的场景下），使用文件锁也能达到相同的效果。

import atexit
import fcntl
 
def init():
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)   # 加锁
        scheduler = BackgroundScheduler()
        def my_job():
            print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        scheduler.add_job(my_job, 'interval', seconds=10)
        scheduler.start()
    except:
        pass
    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)   
        f.close()
    atexit.register(unlock)     # 释放锁

init()  # 执行函数
复制
socket锁
这个方案在此处就不写了，具体可以参考stackoverflow上的方案。这个方案也是可行的，就是需要浪费一个端口。

参考资料

http://blog.csdn.net/raptor/article/details/69218271
http://h4ck.org.cn/2019/01/django-apscheduler-uwsgi-%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1%E9%87%8D%E5%A4%8D%E8%BF%90%E8%A1%8C/
本文参与 腾讯云自媒体分享计划 ，欢迎热爱写作的你一起参与！