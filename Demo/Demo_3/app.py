from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# 设置app.config中关于数据库的参数
# SQLAlchemy(app)会自动从app.config中读取数据库的配置
# MySQL所在的主机名
HOSTNAME = '127.0.0.1'
# MySQL的监听端口号，默认3306
PORT = '3306'
# MySQL的用户名，在安装MySQL时由用户创建
USERNAME = 'root'
# MySQL的密码，在安装MySQL时由用户创建
PASSWORD = 'huang33280234'
# MySQL的数据库名
DATABASE = 'flask_web'

# 创建app应用
app = Flask(__name__)
# 应用到app.config中
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
# 连接SQLAlchemy到Flask应用
db = SQLAlchemy(app)

# 测试数据库是否已连接
# with db.engine.connect() as conn:
# 	# 使用text函数将字符串转换为可执行的SQLAlchemy对象
# 	rs = conn.execute(text('select 1'))
# 	print(rs.fetchone())  # Success : (1,)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # varchar
    password = db.Column(db.String(80), nullable=False)


with app.app_context():
    db.create_all()  # 同步至数据库


@app.route('/')
def hello_world():
    return 'Hello World'

#####  INSERT  #####


@app.route('/add_user')
def add_user():
    # 创建ORM对象
    user_sam = User(id=1, username='sam',
                    password='i will set the seas ablaze')
    user_firefly = User(id=2, username='firefly',
                        password='i dreamed of a scorched earth')
    # 将ORM对象添加到db.session中
    db.session.add(user_sam)
    db.session.add(user_firefly)
    # 将db.session中的所有ORM对象同步到数据库
    db.session.commit()
    return 'Add User Success'
#####  INSERT  #####


#####  QUERY  #####
@app.route('/get_user')
def get_user():
    output = {}
    # 查找对象：根据主键查找
    query_user_key = User.query.get(1)
    # 由于query_user_key是根据主键查找，所以只有一条记录
    print(f'使用主键查询：\n'
          f'ID : {query_user_key.id} , '
          f'Username : {query_user_key.username} , '
          f'Password : {query_user_key.password}')

    # 查找对象：根据条件查找
    query_user_filter = User.query.filter_by(username='firefly')
    # 使用for循环获取query_user_filter的每一条记录
    for user in query_user_filter:
        print(f'使用for循环获取全部记录：\n'
              f'ID : {user.id} , Username : {user.username} , Password : {user.password}')
    # 使用first()获取query_user_filter的第一条记录
    query_user_filter_first = query_user_filter.first()
    print(f'使用first()获取第一条记录：\n'
          f'First User : ID : {query_user_filter_first.id} , '
          f'Username : {query_user_filter_first.username} , '
          f'Password : {query_user_filter_first.password}')

    return 'Get User Success'
#####  QUERY  #####


#####  UPDATE  #####
@app.route('/update_user')
def update_user():
    # 查找到需要删除的对象
    user_update = User.query.filter_by(username='firefly').first()
    user_update.password = '我梦见一片焦土'
    # 同步到数据库中
    # 由于username='fireflt'的记录已经在add_user()中添加至sessions，因此直接提交即可
    db.session.commit()

    return 'Update User Success'
#####  UPDATE  #####


#####  DELETE  #####
@app.route('/delete_user')
def delete_user():
    # 查找到需要删除的对象——主键查询
    user_delete = User.query.get(1)
    # 从Sessions中删除对象
    db.session.delete(user_delete)
    # 同步到数据库中
    db.session.commit()

    return 'Delete User Success'
#####  DELETE  #####


if __name__ == '__main__':
    app.run(debug=True)
