## 这是一个基于Django 开发的简单博客系统。
## 该应用已实现：博客展示、评论、搜索、文章分类等功能。应用基于模板系统，前后端未分离。
## 同时也开发了一套 restful api，地址位于： http://blog.frankxiang.xyz/api/v1/

## 简单的使用方法：

创建虚拟环境

使用pip安装第三方依赖

修改settings.example.py文件为settings.py，添加相应保密参数

运行migrate命令，创建数据库和数据表。

确保 Mysql, Redies, elasticsearch 服务正在运行。

运行python manage.py runserver启动服务器。