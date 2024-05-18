from flask import Flask
from flask_sqlalchemy import SQLAlchemy

## 设置app.config中关于数据库的参数
## SQLAlchemy(app)会自动从app.config中读取数据库的配置
# MySQL所在的主机名
HOSTNAME = '127.0.0.1'
# MySQL的监听端口号，默认3306
PORT = '3306'
# MySQL的用户名，在安装MySQL时由用户创建
USERNAME = 'root'
# MySQL的密码，在安装MySQL时由用户创建
PASSWORD = '9966330'
# MySQL的数据库名
DATABASE = 'flask-web'

# 创建app应用
app = Flask(__name__)
# 应用到app.config中
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
# 连接SQLAlchemy到Flask应用
db = SQLAlchemy(app)

# 表：作者
class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)

# 表：文章
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加作者ID的外键
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))  # author_id 为外键，关联author表中的id字段
    # 模型关系：作者与文章是一对多的关系。会自动处理外键关联
    # backref：反向引用，会自动给Article模型添加一个articles属性,可以通过Author.articles访问Article表中的数据
    author = db.relationship('Author',backref='articles')

# 同步至数据库
with app.app_context():
    db.create_all()

@app.route('/add_author/<name>')
def add_author(name):
    author = Author(name=name)

    # 添加到db.session中
    db.session.add(author)
    # 提交
    db.session.commit()

    return 'Add Author Success'

@app.route('/add_article')
def add_article():
    article_1 = Article(title='Firefly_1', content='我梦见一片焦土')
    article_1.author = Author.query.get(1)
    article_2 = Article(title='Firefly_2', content='一株破土而出的新蕊')
    article_2.author = Author.query.get(1)

    # 添加到db.session中
    db.session.add(article_1)
    db.session.add(article_2)
    # 提交
    db.session.commit()

    return 'Add Article Success'

@app.route('/get_author/<int:id>')
def get_article(id):
    author = Author.query.get(id)
    articles = author.articles

    for art in articles:
        print(f'Title:{art.title}, Content:{art.content}')

    return 'Get Articles Success'


if __name__ == '__main__':
    app.run(debug=True)