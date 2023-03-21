Django 不到20行代码实现用户认证及权限管理完整功能

__弯弓__

已于 2022-12-08 18:23:39 修改

576
 收藏 5
文章标签： django python 后端
版权
1、用户认证与权限管理 — 绕不过去的需求
几乎所有软件项目都不得不实现的1个功能需求就是：用户认证与权限管理。其基本要求包括：

提供用户登入，登出，密码更改，密码重置等页面。
对页面操作、数据访问的权限控制，包括增删改查。
权限控制基于用户、组、基于页面、基于表。
说起来容易，实现起来却非易事，特别是权限控制，很多程序员提起权限细化都头痛。

需要先赞一下Django的用户认证与权限子系统，认认真真地落实 不重复发明轮子(Don’'t Re-invent Yourself) 理念，让程序猿们可以集中精力于业务逻辑的开发。下面就介绍，如何利用 django auth模块内置视图与组件，快速完成用户认证及权限控制的开发。

2、Django演示项目环境准备
2.1 运行环境准备
为了初学者阅读方便，还是加上这一节吧

新建1个项目
django-admin startproject myproject

新建app, 在此笔者创建的app名称为 imgproc
cd myproject
python manage.py startapp imgproc

将app添加到项目配置文件
在setting.py 中将新建app加入INSTALLED_APPS

INSTALLED_APPS = [
	......
    'imgproc',
]
1
2
3
4
同步数据库

python manage.py makemigrations
python manage.py migrate

运行项目
python manage.py runserver， 默认端口 8000
这时应该可以访问 http://127.0.0.1:8000/ 了。

创建管理员帐号
python manage.py createsuperuser
访问http://127.0.0.1:8000/admin/ 检查登录是否正常。

至此，项目运行环境创建就算完成了。

2.2 演示项目准备
演示项目的代码及数据包括：，

创建1个model UploadFile
视图函数与视图类
URL config
模板文件
数据库测试数据
2.2.1 在imgproc应用中添加模型， models.py
# models.py 
from django.db import models
from django.urls import reverse

# Create your models here.
class UploadFile(models.Model):
    title = models.CharField(max_length=30)
    uploadfile = models.ImageField(upload_to="upload/")
    
    def __str__(self) -> str:
        return self.title
1
2
3
4
5
6
7
8
9
10
11
2.2.2 将model 加入后台 admin.py
from django.contrib import admin
from  imgproc.models import *
# Register your models here.

class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['id','title','uploadfile']

admin.site.register(UploadFile,UploadFileAdmin)
1
2
3
4
5
6
7
8
2.2.3 编写视图函数与视图类 views.py
为了演示，使用了内置通用视图方式与函数式编程两个视图，可能你都会用到。

from django.shortcuts import render,redirect
from django.http import HttpResponse, FileResponse
# Create your views here.
from imgproc.forms import *
from imgproc.models import *
from django.views import generic
from django.urls import reverse_lazy
import os

class UploadfileListView(generic.ListView):
    """list all data """
    model = UploadFile
    template_name = "imgproc/uploadfile_list.html"

   
def download_file_stream(request,fid=1):
    """ Send file with FileResponse """
    obj = UploadFile.objects.get(pk=fid)
    fpath = os.path.join(settings.MEDIA_ROOT, obj.uploadfile.name)
    print(fpath)
    response = FileResponse(open(fpath,'rb' ))
    response['Content-Type'] = 'application/octet-stream'
    response["Content-Disposition"] = "attachment; filename=test.jpg"
    return response
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
2.2.4 URL config 配置
myproject/myproject/urls.py

from django.contrib import admin
from django.urls import path,re_path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('image/',include("imgproc.urls")),
]

1
2
3
4
5
6
7
8
imgproc.urls.py 代码

from django.urls import path,re_path
from imgproc.views import *

urlpatterns = [
name="upload_file_update"),
    path("list/", UploadfileListView.as_view(), name="upload_file_list" ),
    path("download/<int:fid>/",download_file_stream, name="download_file" ), 
]

1
2
3
4
5
6
7
8
9
2.2.5 编写显示数据的模板
在imgproc 下新建模板目录
mkdir templates/imgproc/ 子目录，创建template 文件 uploadfile_list.html, base.html 里引入了bootsrap4 来渲染

{% comment %}  uploadfile_list.html {% endcomment %}
{% extends './base.html' %}
{% block content %}
{% load static %}
    <div class="p-3 align-self-center border border-1 bg-light shadow-lg ">
        <h2>uploadfiles </h2>
        <ul class="list-group">
            {% for d in object_list %}
                <li class="list-group-item"> {{ d.id }} , {{ d.title }} , {{ d.uploadfile }} </li>
            {% endfor %}
        </ul>
    </div>

{% endblock %}  

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
2.2.6 添加测试数据并测试URL
通过 http://127.0.0.1:8000/admin/ , django 管理后台, 添加一些测试数据。
通过 http://127.0.0.1:8000/image/list/ 可以显示所有数据

通过http://127.0.0.1:8000/image/download/1/ 可以下载图片。

3、用django内置视图完成用户认证
django.contrib.auth 用户认证模块内置了 User 模型与一套用户认证视图，直接使用这些组件开发，让用户认证变得异常简单，下面我们来看一下实现过程

3.1 导入内置视图的url
将auth模块的内置视的url加入在项目的urls,.py 中， 也就是myproject/myproject/urls.py 中添加：

urlpatterns = [
    ...., 
    path("accounts/", include("django.contrib.auth.urls")),  # new
]
1
2
3
4
3.2 添加 login.html 登录模板
在项目根目录下，创建模板目录
mkdir templates/registration/
cd templates/registration/
新建 login.html

...
<h2> 请登录 </h2>
<form method="POST">
       {% csrf_token %}
       {{ form.as_p}}
      <input type="submit" class="btn btn-success" value="登录">
</form>
...
1
2
3
4
5
6
7
8
另外要为logout 登出后指定前转页面，在项目的配置文件 myproject/myproject/settings.py 中添加配置

LOGOUT_REDIRECT_URL = "/account/login/"        # 登出后重定向页面
1
3.3 Django内置认证视图提供的url
在URL config中添加了include("django.contrib.auth.urls") 之后，就可以使用以下用户认址的URL 接口了， 包含用户登录，登出，修改密码，密码确认，重置密码等页面。

accounts/login/ [name='login']   
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
1
2
3
4
5
6
7
8
3.4 测试
尝试一下用管理员帐户登录

http://127.0.0.1:8000/accounts/login/ 
1
以及修改密码等URL

总共只用了2行代码，就完成了用户认证的后端开发，是不是很神奇。而且由于 django还是以安全性著称的，实现的这些接口安全性也可有效保证。

4、权限管理的实现
本文开头提到，权限管理需求包含： 基于页面操作与数据操作的权限控制， 下面分别介绍如何实现

4.1 基于URL页面的权限控制
思路就是，当用户访问url 页面时，先检查其是否已登录，如果没有登录或用户名密码不对，前转到登录页面。

实现这1过程也非常简单
对于视图函数，前加1个装饰器 @login_required 即可

from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def download_file_stream(request,fid=1):
    ......
1
2
3
4
5
实现功能： 如果request请求中的user 参数已登录过，则继续运行后面的语句，否则跳转到登录页面。

对于类方式实现的视图类，提供了LoginRequiredMixin基类，视图类用多继承方式来实现

from django.contrib.auth.mixins import LoginRequiredMixin

class MyView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
1
2
3
4
注：LoginRequiredMixin一定要写在 ListView前面。

4.2 基于用户、表(模型）的数据访问权限
4.2.1 Django 用户数据权限管理的基本逻辑
当通过 makemigration 命令向数据库添加模型（表）时，默认为每个 Django 模型创建了四个权限：添加add、修改change、删除delete 和查看view。

在数据库的 auth_permission表中，每张表都有4个权限： add, change, delete, view,
比如，对于演示项目的 Uploadfile 模型来说，当在数据库中生成表时， 会在权限表 auth_permission 中，为Uploadfile 添加 4个权限，codename 字段值分别为：

view_uploadfile
add_uploadfile
change_uploadfile
delete_uploadfile
当你在管理后台，创建用户时，会列出上面的4个权限供选择。
如果打开数据库，会发现 User表与auth_permission 权限表是1对多关系，因此还有1张表: auth_user_permission 关系表，记录了每个user的赋予的权限。 可以通过该表查询具体的权限，

4.2.2 如何给用户添加数据操作权限
在管理后台创建新用户时，添加权限，每张表都可以指定增删改查权限。无须编程实现。

可以进入 python manage,py shell 来检验一下用户权限（可以跳过此步），
如下例 ，新建用户test01， 在模型 uploadfile上有add权限，但没有 user模型的add权限， 对于 test01 用户，可以用 has_perm()方法来验证其在 两个模型上的权限

In [13]: user1 = User.objects.get(username="test01")
In [15]: user1.has_perm("imgproc.add_uploadfile")
Out[15]: True
In [16]: user1.has_perm("imgproc.add_user")
Out[16]: False
1
2
3
4
5
4.2.3 数据操作权限控制的实现
当客户端通过URL来访问数据时，如何判断用户是否有相应的操作权限呢？
**对于视图函数，**使用permission_required 装饰器来检查用户是否有权限。

from django.contrib.auth.decorators import permission_required

@permission_required('imgproc.view_uploadfile')
#@permission_required(('imgproc.add_uploadfile')
def download_file(request,fid=1):
   # …

1
2
3
4
5
6
7
如果要多检查1项权限，只须再添加1条装饰器语句。

对于视图类，提供了PermissionRequiredMixin基类，通过多继承方式实现：

from django.contrib.auth.mixins import PermissionRequiredMixin

class UploadfileListView(PermissionRequiredMixin,generic.ListView):
    """list all data if user has view permission """
     permission_required = ('imgproc.view_uploadfile', )
1
2
3
4
5
最多3行代码，就提供了完整的基于用户，基于表的数据操作权限控制。

@permission_required 失败会前转登录页面，(HTTP Status 302).
＠PermissionRequiredMixin 失入发送403 (HTTP Status Forbidden).

5、总结
Django 的用户认证与权限子系统提供了1种快速实现的方式，只用了不到 20 行代码，就为项目添加了一套相当完善的用户认证与权限控制功能。
如果要对用户认证或权限做更深入的功能开发，如基于字段控制权限，就需要进一步理解 django 框架模型类，User类， Permission类的基本工作原理，django也提供了丰富的接口用于定制化开发。
————————————————
版权声明：本文为CSDN博主「__弯弓__」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/captain5339/article/details/128234437