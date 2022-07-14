# 整到page41，创建、读取、更新、删除

import os
from re import T
import sys

from flask import Flask
from flask import render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

import click


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

@app.cli.command() #注册为命令，在app注册之后使用，不然会undefined
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    # intitialize the database
    if drop: #判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息

class User(db.Model):   #表格名称将会是user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key = True)  #主键
    name = db.Column(db.String(20)) #名字

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True) #主键
    title = db.Column(db.String(60)) #电影标题
    year = db.Column(db.String(4)) #电影年份

@app.cli.command() #注册为命令，在app注册之后使用，不然会undefined
def forge():
    """Generate fake data"""
    db.create_all()
    name = 'Leo Wong'
    movies = [
        {'title': 'My neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name = name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title = m['title'], year = m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('fake data Done.')

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)
# @app.route('/index')
# @app.route('/home')
# def hello():
#     return 'Welcome to My Watchlist!'
    # return u'欢迎来到我的Watchlist!'
    # return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    
@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name = 'Leo Wong'))
    print(url_for('user_page', name = 'Peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num = 2))
    return 'Test page'
