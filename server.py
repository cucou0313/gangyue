from flask import Flask, redirect, url_for, render_template, request, make_response
# url_for()函数对于动态构建特定函数的URL非常有用。该函数接受函数的名称作为第一个参数，以及一个或多个关键字参数，每个参数对应于URL的变量部分。
import pymysql
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0313@localhost/gangyue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 使用flask_sqlalchemy进行主页数据访问，便于分页pagination的使用
db = SQLAlchemy(app)
# 使用pymysql方式进行登录注册的连接，防止连接池过多
sqlconn = {
    'host': 'localhost',
    'user': 'root',
    'password': '0313',
    'database': 'gangyue'
}
# pythonanywherede 连接MySQL
# NAME：pythonanywhere用户名+$+数据库名  cucou0313$gangyue
# USER：pythonanywhere用户名 cucou0313
# HOST：pythonanywhere用户名+.mysql.pythonanywhere-services.com  cucou0313.mysql.pythonanywhere-services.com
# sqlconn = {
#     'host': 'cucou0313.mysql.pythonanywhere-services.com',
#     'user': 'cucou0313',
#     'password': 'gangyue6',
#     'database': 'cucou0313$gangyue'
# }


@app.route('/')
def welcome():
    return render_template('welcome.html')


# 登录方法，连接MySQL进行账号验证
@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        pymysql_db = pymysql.connect(host=sqlconn['host'],
                                     user=sqlconn['user'],
                                     password=sqlconn['password'],
                                     database=sqlconn['database'])
        # userId = request.form['userId']
        # userPsd = request.form['userPsd']
        userId = request.form.get('Id')
        userPsd = request.form.get('Psd')
        # if userId is not None and userPsd is not None:
        sql = "SELECT * FROM user WHERE student_id = %s and password = %s" % (
            userId, userPsd)
        cursor = pymysql_db.cursor()
        try:
            res = cursor.execute(sql)
            # fetchone为空时的返回集为None
            # res = cursor.fetchone()
            # if res is None:
            if res:
                sqlData = cursor.fetchone()
                # 验证通过，保存cookie并跳转至主页面
                # resp = make_response("redirect(url_for('main'))")
                # 登录时顺带传递name
                userName = sqlData[2]
                resp = make_response(userName)
                resp.set_cookie('userId', userId)
                resp.set_cookie('userName', userName)
                resp.set_cookie('userPsd', userPsd)
                return resp
            else:
                # 登录失败时，通过Ajax返回
                return "User info error"
        except Exception as e:
            print('error', e)
        finally:
            cursor.close()
            pymysql_db.close()
    elif request.method == 'GET':
        return render_template('sign_in.html')


# 注册方法，连接MySQL写入
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        pymysql_db = pymysql.connect(host=sqlconn['host'],
                                     user=sqlconn['user'],
                                     password=sqlconn['password'],
                                     database=sqlconn['database'])
        userId = request.form.get('Id')
        userName = request.form.get('Name')
        userPsd = request.form.get('Psd')
        userIdvalid = False
        sql = "SELECT * FROM user WHERE student_id = %s" % (userId)
        cursor = pymysql_db.cursor()
        try:
            res = cursor.execute(sql)
            if res:
                return "User id has exist"
            else:
                userIdvalid = True
        except Exception as e:
            print('error', e)
        finally:
            if userIdvalid:
                sql = "INSERT INTO user(student_id,name,password) VALUES ('%s', '%s', '%s')" % (
                    userId, userName, userPsd)
                cursor.execute(sql)
                pymysql_db.commit()
                cursor.close()
                pymysql_db.close()
                return "Register success"
        # 注册成功，跳转至主页面
        # return redirect(url_for('sign_in'))
    elif request.method == 'GET':
        return render_template('sign_up.html')


# 建立flask_sqlalchemy的模型，对应mysql的Post表
class Post(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    title = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    added_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=1)
    is_knot = db.Column(db.Integer, nullable=False, default=0)


@app.route('/main/<int:page>', methods=['POST', 'GET'])
def main(page=1):
    userName = request.cookies.get('userName')
    paginate = Post.query.order_by('added_time').paginate(page,
                                                          per_page=10,
                                                          error_out=False)
    data = {
        'userName': userName,
        'pagination': paginate,
        'posts': paginate.items
    }
    return render_template('main.html', **data)


@app.route('/search/<int:page>', methods=['POST', 'GET'])
def search(page=1):
    if request.method == 'POST':
        searchValue = request.form.get('searchValue')
        paginate = Post.query.filter(
            Post.title.like('%{searchValue}%'.format(
                searchValue=searchValue))).order_by('added_time').paginate(
                    page, per_page=10, error_out=False)
        data = {'pagination': paginate, 'posts': paginate.items}
        resp = make_response(render_template('search.html', **data))
        resp.set_cookie('searchValue', searchValue)
        return resp
    else:
        searchValue = request.cookies.get('searchValue')
        paginate = Post.query.filter(
            Post.title.like('%{searchValue}%'.format(
                searchValue=searchValue))).order_by('added_time').paginate(
                    page, per_page=10, error_out=False)
        data = {'pagination': paginate, 'posts': paginate.items}
        return render_template('search.html', **data)


@app.route('/user_info')
def user_info():
    userName = request.cookies.get('userName')
    userPsd = request.cookies.get('userPsd')
    return render_template('user_info.html',
                           userName=userName,
                           userPsd=userPsd)


# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('login'), 302)

if __name__ == '__main__':
    # 将debug = True可在debug模式中自动重启服务
    app.debug = True
    app.run(host='localhost', port=5000)