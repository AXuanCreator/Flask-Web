# Flask-Web Code

本文件夹 `/code` 为该项目的主体，仅实现服务端部分和部分客户端功能，使用Jinja模板



Flask文档：[流萤小姐教你如何学习Flask](https://dormousehole.readthedocs.io/en/latest/index.html)

Flask-SQLAlchemy文档：[萨姆大哥教你如何点燃数据库](https://wizardforcel.gitbooks.io/flask-extension-docs/content/flask-sqlalchemy.html)

Flask与Jinja2协同：[Jinja2中文文档](https://docs.pythontab.com/jinja/jinja2/)



## 环境配置

```cmd
conda create -n flask-web python=3.10 -y

conda activate flask-web

conda install flask pymysql flask-sqlalchemy flask_cors  -y 

pip install flask_migrate flask_caching flask_mail

# OPTION
conda install pytorch tqdm pandas -y 	# 基于深度学习的书籍推荐
```



## 注意事项

需要在Pycharm中将Flask-Web/Code文件夹设置为 **源代码根目录**，一切相对路径都是相对于Code文件夹。否则将会出现导入包路径错误但依旧能正常运行



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



