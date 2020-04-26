from flask import Flask, redirect, url_for, render_template, request, make_response, jsonify
# url_for()函数对于动态构建特定函数的URL非常有用。该函数接受函数的名称作为第一个参数，以及一个或多个关键字参数，每个参数对应于URL的变量部分。
import pymysql
# import mysql.connector
import time
import datetime
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
app = Flask(__name__)

databasePWD = '0313'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + databasePWD + '@localhost/gangyue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 使用flask_sqlalchemy进行主页数据访问，便于分页pagination的使用
db = SQLAlchemy(app)
# 使用pymysql方式进行登录注册的连接，防止连接池过多
sqlconn = {
    'host': 'localhost',
    'user': 'root',
    'password': databasePWD,
    'database': 'gangyue'
}

dbengine = create_engine('mysql+pymysql://root:' + databasePWD +
                         '@localhost/gangyue')

# pythonanywherede 连接MySQL
# NAME：pythonanywhere用户名+$+数据库名	 cucou0313$gangyue
# USER：pythonanywhere用户名 cucou0313
# HOST：pythonanywhere用户名+.mysql.pythonanywhere-services.com	 cucou0313.mysql.pythonanywhere-services.com
# sqlconn = {
#	  'host': 'cucou0313.mysql.pythonanywhere-services.com',
#	  'user': 'cucou0313',
#	  'password': 'gangyue6',
#	  'database': 'cucou0313$gangyue'
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

        student_id = request.form.get('Id')
        userPsd = request.form.get('Psd')
        # if userId is not None and userPsd is not None:
        sql = "SELECT * FROM user WHERE student_id = %s and password = '%s'" % (
            student_id, userPsd)
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
                userId = sqlData[0]
                resp = make_response(userName)
                resp.set_cookie('student_id', student_id)
                resp.set_cookie('userName', userName)
                resp.set_cookie('userId', str(userId))
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
    __tablename__ = 'post'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    title = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    added_time = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=1)
    is_knot = db.Column(db.Integer, nullable=False, default=0)


class PostName(db.Model):
    __tablename__ = 'postname'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    title = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    added_time = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=1)
    is_knot = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(20), nullable=False)


# @app.route('/main/<int:page>', methods=['POST', 'GET'])
# def main(page=1):
#     userName = request.cookies.get('userName')
#     student_id = request.cookies.get('student_id')
#     paginate = Post.query.order_by(Post.added_time.desc()).paginate(
#         page, per_page=10, error_out=False)
#     data = {
#         'userName': userName,
#         'student_id': student_id,
#         'pagination': paginate,
#         'posts': paginate.items,
#         'url': 'main'
#     }
#     print(data)
#     return render_template('main.html', **data)


@app.route('/reply', methods=['POST'])
def reply():
    postId = request.form.get('postId')
    student_id = request.cookies.get('student_id')
    pymysql_db = pymysql.connect(host=sqlconn['host'],
                                 user=sqlconn['user'],
                                 password=sqlconn['password'],
                                 database=sqlconn['database'],
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM reply,user WHERE user_id=user.id and post_id = '%s' order by added_time asc" % (
        postId)
    cursor = pymysql_db.cursor()
    res = cursor.execute(sql)
    sqlData = cursor.fetchall()
    data = {'replys': sqlData, 'student_id': student_id}
    cursor.close()
    pymysql_db.close()
    return render_template('reply.html', **data)


@app.route('/add_reply', methods=['POST'])
def add_reply():
    pymysql_db = pymysql.connect(host=sqlconn['host'],
                                 user=sqlconn['user'],
                                 password=sqlconn['password'],
                                 database=sqlconn['database'],
                                 cursorclass=pymysql.cursors.DictCursor)
    postId = request.form.get('postId')
    replytext = request.form.get('replytext')
    userId = request.cookies.get('userId')
    student_id = request.cookies.get('student_id')
    added_time = datetime.datetime.now()
    sql = "INSERT INTO reply(content,added_time,post_id,user_id) VALUES ('%s', '%s','%s', '%s')" % (
        replytext, added_time, postId, userId)
    cursor = pymysql_db.cursor()
    try:
        cursor.execute(sql)
        pymysql_db.commit()
    except Exception as e:
        print('error', e)
    finally:
        sql = "SELECT * FROM reply,user WHERE user_id=user.id and post_id = '%s' order by added_time asc" % (
            postId)
        res = cursor.execute(sql)
        sqlData = cursor.fetchall()
        data = {'replys': sqlData, 'student_id': student_id}
        cursor.close()
        pymysql_db.close()
        return render_template('reply.html', **data)


@app.route('/chat', methods=['POST'])
def chat():
    other_id = request.form.get('other_id')
    other_name = request.form.get('other_name')
    userId = request.cookies.get('userId')
    userName = request.cookies.get('userName')
    pymysql_db = pymysql.connect(host=sqlconn['host'],
                                 user=sqlconn['user'],
                                 password=sqlconn['password'],
                                 database=sqlconn['database'],
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM chat_record WHERE (from_user_id='%s' and to_user_id='%s') or (from_user_id='%s' and to_user_id='%s') order by added_time asc" % (
        other_id, userId, userId, other_id)
    cursor = pymysql_db.cursor()
    res = cursor.execute(sql)
    sqlData = cursor.fetchall()
    data = {
        'chats': sqlData,
        'other_name': other_name,
        'userName': userName,
        'other_id': other_id,
        'userId': int(userId)
    }
    print(data)
    cursor.close()
    pymysql_db.close()
    return render_template('chat.html', **data)


@app.route('/knot_post', methods=['POST'])
def knot_post():
    postid = request.form.get('postid')
    pymysql_db = pymysql.connect(host=sqlconn['host'],
                                 user=sqlconn['user'],
                                 password=sqlconn['password'],
                                 database=sqlconn['database'])
    sql = "UPDATE post SET is_knot=1 WHERE id='%s'" % (postid)
    try:
        cursor = pymysql_db.cursor()
        cursor.execute(sql)
        pymysql_db.commit()
    except Exception as e:
        print('error', e)
    finally:
        cursor.close()
        pymysql_db.close()
        return render_template('knot.html')


@app.route('/add_chat', methods=['POST'])
def add_chat():
    pymysql_db = pymysql.connect(host=sqlconn['host'],
                                 user=sqlconn['user'],
                                 password=sqlconn['password'],
                                 database=sqlconn['database'],
                                 cursorclass=pymysql.cursors.DictCursor)
    other_id = request.form.get('other_id')
    chattext = request.form.get('chattext')
    userId = request.cookies.get('userId')
    userName = request.cookies.get('userName')
    other_name = request.form.get('other_name')
    added_time = datetime.datetime.now()
    sql = "INSERT INTO chat_record(content,added_time,from_user_id,to_user_id) VALUES ('%s', '%s','%s', '%s')" % (
        chattext, added_time, userId, other_id)
    cursor = pymysql_db.cursor()
    try:
        cursor.execute(sql)
        pymysql_db.commit()
    except Exception as e:
        print('error', e)
    finally:
        sql = "SELECT * FROM chat_record WHERE (from_user_id='%s' and to_user_id='%s') or (from_user_id='%s' and to_user_id='%s') order by added_time asc" % (
            other_id, userId, userId, other_id)
        cursor = pymysql_db.cursor()
        res = cursor.execute(sql)
        sqlData = cursor.fetchall()
        data = {
            'chats': sqlData,
            'other_name': other_name,
            'userName': userName,
            'other_id': other_id,
            'userId': int(userId)
        }
        print(data)
        cursor.close()
        pymysql_db.close()
        return render_template('chat.html', **data)


# 带分类的main
@app.route('/main/<string:category>/<int:page>', methods=['POST', 'GET'])
def main(category='all', page=1):
    userName = request.cookies.get('userName')
    student_id = request.cookies.get('student_id')
    userId = request.cookies.get('userId')
    if category == 'all':
        paginate = PostName.query.order_by(
            PostName.added_time.desc()).paginate(page,
                                                 per_page=10,
                                                 error_out=False)
    elif category == 'mine':
        paginate = Post.query.filter(Post.user_id == userId).order_by(
            Post.added_time.desc()).paginate(page,
                                             per_page=10,
                                             error_out=False)
    elif category == 'others':
        paginate = Post.query.filter(Post.user_id != userId).order_by(
            Post.added_time.desc()).paginate(page,
                                             per_page=10,
                                             error_out=False)
    else:
        paginate = Post.query.filter(Post.category == category).order_by(
            Post.added_time.desc()).paginate(page,
                                             per_page=10,
                                             error_out=False)
    data = {
        'userName': userName,
        'student_id': student_id,
        'userId': int(userId),
        'pagination': paginate,
        'posts': paginate.items,
        'url': 'main',
        'category': category
    }
    print(data)
    return render_template('main.html', **data)


@app.route('/search/<int:page>', methods=['POST', 'GET'])
def search(page=1):
    if request.method == 'POST':
        searchValue = request.form.get('searchValue')
        userName = request.cookies.get('userName')
        student_id = request.cookies.get('student_id')
        userId = request.cookies.get('userId')
        paginate = Post.query.filter(
            Post.title.like('%{searchValue}%'.format(
                searchValue=searchValue))).order_by('added_time').paginate(
                    page, per_page=10, error_out=False)
        data = {
            'pagination': paginate,
            'posts': paginate.items,
            'userName': userName,
            'student_id': student_id,
            'userId': int(userId)
        }
        resp = make_response(render_template('search.html', **data))
        resp.set_cookie('searchValue', searchValue)
        return resp
    else:
        searchValue = request.cookies.get('searchValue')
        userName = request.cookies.get('userName')
        student_id = request.cookies.get('student_id')
        userId = request.cookies.get('userId')
        paginate = Post.query.filter(
            Post.title.like('%{searchValue}%'.format(
                searchValue=searchValue))).order_by('added_time').paginate(
                    page, per_page=10, error_out=False)
        data = {
            'pagination': paginate,
            'posts': paginate.items,
            'userName': userName,
            'student_id': student_id,
            'userId': int(userId)
        }
        return render_template('search.html', **data)


@app.route('/user_info', methods=['GET'])
def user_info():
    student_id = request.cookies.get('student_id')
    pymysql_db = pymysql.connect(host=sqlconn['host'],
                                 user=sqlconn['user'],
                                 password=sqlconn['password'],
                                 database=sqlconn['database'],
                                 cursorclass=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM user WHERE student_id = %s" % (student_id)
    cursor = pymysql_db.cursor()
    res = cursor.execute(sql)
    sqlData = cursor.fetchone()
    data = {
        'userinfo': sqlData,
    }
    print(data)
    cursor.close()
    pymysql_db.close()
    return render_template('user_info.html', **data)


@app.route('/post_new', methods=['POST', 'GET'])
def post_new():
    if request.method == 'GET':
        return render_template('post_new.html')
    if request.method == 'POST':
        userName = request.cookies.get('userName')
        userPsd = request.cookies.get('userPsd')
        new_data = str(request.get_data(), encoding='utf-8')
        print(userName, userPsd, new_data)

        try:
            new_data = json.loads(new_data)
            category = new_data["category"]
            content = new_data["content"]
            title = new_data["title"]
            added_time = datetime.datetime.now()
            userId = request.cookies.get('userId')
            DBsession = sessionmaker(bind=dbengine)
            session = DBsession()

            post = Post(category=category,
                        title=title,
                        content=content,
                        added_time=added_time,
                        user_id=userId)

            session.add(post)
            session.commit()
            session.close()
        except err:
            if err:
                print(err)
            return 'param  error', 403

        return "OK", 200


@app.route('/logout')
def logout():
    response = make_response(render_template('welcome.html'))
    response.delete_cookie('student_id')
    response.delete_cookie('userId')
    response.delete_cookie('userName')
    response.delete_cookie('userPsd')
    response.delete_cookie('searchValue')
    return response


if __name__ == '__main__':
    # 将debug = True可在debug模式中自动重启服务
    app.debug = True
    app.run(host='localhost', port=5000)
