from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ORM模型——USER


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    password = db.Column(db.String(80), nullable=True)
    data = db.Column(db.DateTime, server_default=db.func.now())
