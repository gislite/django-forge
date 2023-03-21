# Django


## 安装

    pip install --upgrade django
    python -m django --version

## 使用

```bash
django-admin startproject mysite
cd mysite
python manage.py migrate
python manage.py runserver
```


## 相关配置

允许远程访问：

修改创建项目时生成的 `setting.py` 文件

将

    ALLOWED_HOSTS = []

改为

    ALLOWED_HOSTS = ['*']


```
python manage.py runserver 0.0.0.0:6799
```

## 创建投票应用 

```bash
python manage.py startapp polls
```

## 改变模型

你只需要记住，改变模型需要这三步：

编辑 models.py 文件，改变模型。
运行 python manage.py makemigrations 为模型的改变生成迁移文件。
运行 python manage.py migrate 来应用数据库迁移。

## 交互

```
python manage.py shell
```

## 创建一个管理员账号


首先，我们得创建一个能登录管理页面的用户。请运行下面的命令：


```
python manage.py createsuperuser
```

