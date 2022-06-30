from flask import Flask
from flask import url_for
app = Flask(__name__)

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return 'Welcome to My Watchlist!'
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
