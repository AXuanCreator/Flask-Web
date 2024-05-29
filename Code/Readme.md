# Flask-Web Code

本文件夹 `/code` 为该项目的主体，仅实现服务端部分



Flask文档：[流萤小姐教你如何学习Flask](https://dormousehole.readthedocs.io/en/latest/index.html)

Flask-SQLAlchemy文档：[萨姆大哥教你如何点燃数据库](https://wizardforcel.gitbooks.io/flask-extension-docs/content/flask-sqlalchemy.html)

Flask与Jinja2协同：[Jinja2中文文档](https://docs.pythontab.com/jinja/jinja2/)



## 环境配置

* 未完成，可以加各种奇怪的库，但需在这里写清楚，优先使用conda安装

```cmd
conda create -n flask-web python=3.10 -y

conda activate flask-web

conda install flask pymysql flask-sqlalchemy flask_cors -y 

pip install flask-migrate
```



## 代码规范

采用 **PEP 拔万** ~~先进~~ 的代码格式替代邪教徒PEP 8

### 类名——**大驼峰命名法**

```python
class MyClass:
```



### 函数/变量——**小写与下划线**

```python
def my_function():
    my_variable = 10
```



### 文件命名——小写+下划线

```python
my_module.py
```



### 导入库——**标准库>第三方库>自定义库**

```python
# 标准库——不需要额外安装
import os
import sys

# 第三方库——需要额外安装
import numpy as np
import torch

# 自定义库——自己写的
from mymodule import *
```



### 引号——优先 **单引号** `''`

```python
user = 'firefly'
```



### 注释——留意空格

```python
# 这是一个注释
```



### 缩进——**使用TAB缩进等价四空格**

*  ~~落后的PEP 8妄想使用四个空格替代Tab~~
* ~~令人感叹的Google JAVA竟然使用两个空格的缩进~~

```python
123456
	| TAB
```



### 空行——神奇又好用的 **PyCharm**  在设置格式化按钮后会帮你的。尝试 `Shift + Alt + F`

```python
Class MyClass:
    def __init__(self):
        pass
    							# <==  函数之间空一行
    def pass_function(self):
        pass
    							# <==  类后空两行
    
if __name__ == '__main__':
    pass
```



### 不使用的变量名——使用 `_` 占位

```python
def my_func():
    return x, y

_, y = my_func()	# 不使用x
```



### 空格的使用——**运算符两边** 和 变量后

```python
A = B + C

list = [a, b, c, d, e]
```



### 函数注释——三个`"""`神奇的Pycharm会为你生成

```python
def my_func_a():
	"""这是一个函数"""
	pass

def my_func_b(x):
	"""
	这是一个带参数的函数
	:param x: 我不知道
	:return: 我也不知道
	"""
	pass
```



### 大括号

```python
PYTHON没有大括号亲
```





## 代码模板

### 前端返回信息

语法：`request.get_json()`

```python
from flask import Flask, request, jsonity

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':        
        # 获取 JSON 数据
        user_request = request.get_json()

        # 从 JSON 里获取数据
        username = user_request.get('username')
        password = user_request.get('password')
```



### 返回消息给前端

语法：`return jsonify({...})`

```python
response = jsonify({
    'code' ResponseCode.ACCOUNT_NOT_EXIST,
    'message': '1111",
    'result': '10086' 
})

return response
```

使用类管理

```python
class Response:
    @staticmethod
    def response(code, msg, result):
        return jsonify({
            'code': code,
            'message': msg,
            'result': result
        })
        

class ResponseCode:
	BAD_REQUEST = 400
	USERNAME_REPEATED = 401
.....................

return Response.response(ResponseCode.BAD_REQUEST,"Fireflyisbeautiful","SAM")
```





### 使用 methods 管理不同的请求

语法：`methods=['...']`

```python
@app.route('/user/register', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_register():
    if request.method == 'GET':
        print('该罚！')
    
    if request.method == 'DELETE':
        print('你过关！')
```



### 使用蓝图管理URL

Demo6 讲述了蓝图的使用，此处仅放出代码

```python
from flask import Blueprint, Flask

app = Flask(__name__)

# 声明蓝图
user = Blueprint('user', __name__)
book = Blueprint('book', __name__)
admin = Blueprint('admin', __name__)

# 绑定蓝图，url_prefix表示前缀url
app.register_blueprint(user, url_prefix = '/user')
app.register_blueprint(book, url_prefix = '/book')
app.register_blueprint(admin, url_prefix = '/admin')

# 定义视图函数
@user.route('/login')	# /user/login
def login():
    pass
```



### Services层使用 @staticmethod

```python
class UserService:
    @staticmethod
    def get_all_user():
        return User.query.all()
    
# 调用
UserService.get_all_user()
```



### 从ORM模型中对数据库进行操作

```python
# ORM模型
db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'tb_user'
	id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), unique=True, nullable=True)
	password = db.Column(db.String(80), nullable=True)
	name = db.Column(db.String(20), nullable=True)
	gender = db.Column(db.String(20), nullable=True)
	phone = db.Column(db.String(80), unique=True, nullable=True)
	mail = db.Column(db.String(80), unique=True, nullable=True)
	max_borrow_days = db.Column(db.BigInteger, default=-1)  # 若为-1，则说明Service出现问题
	max_borrow_books = db.Column(db.BigInteger, default=-1)
	creation_date = db.Column(db.DateTime, server_default=db.func.now())  # server_default有更高优先级


## SELECT ##
# 获取所有信息
User.query.all()

# 通过id获取信息
User.query.get(id)

# 通过指定字段获取信息
# 假如username并非unique并且有多人昵称为Firefly，就需要通过迭代、first()、second()等方法获取ORM对象
User.query.filter_by(username='Firefly')	


## INSERT ##
new_user = User(username='Firefly', password='password', ...)
db.session.add(new_user)	# 暂存 == git add .
db.session.commit()		# 提交 == git commit 

## UPDATE ##
update_user = User.query.get(id)	# 实际上应当把 User.query.get(id) 封装在user_service里
if update_user:
    update_user.name = '我不是流萤'
    update_user.phone = '111111'
    db.session.commit()		# 不需要提交到暂存区，直接commit即可。因为update操作是在暂存区中完成

## DELETE ##
delete_user = User.query.filter_by(username='流萤')	# username应当是unique
if delete_user:
    db.session.delete(delete_user)	# 从暂存区中移除
	db.session.commit()	# 提交
```



## 模块结构

```cmd
D:.
├───Admin
├───Book
│   ├───Borrow
│   ├───Category
│   └───Recommend
├───Config
│   └───__pycache__
├───User
│   └───Mail
└───Utils
```



### User

User登陆

User注册

User个人信息修改

User密码修改

User注销



### Book

Book查询

Book修改

Book增加

Book删除

Book分页



#### Category

增加图书类别

删除图书类别

获取图书类别



#### Recommend

书籍推荐



#### Borrow

Book借阅

Book历史借阅

Book归还

Book续借

Book查询归还状态



### Admin

Admin登陆

Admin查询

Admin个人信息修改

Admin密码修改







## 注意事项

需要将Flask-Web/Code文件夹设置为 **源代码根目录**，一切相对路径都是相对于Code文件夹。否则将会出现导入包路径错误但依旧能正常运行

