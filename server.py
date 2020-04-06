from flask import Flask, redirect, url_for, render_template, request, make_response
# url_for()函数对于动态构建特定函数的URL非常有用。该函数接受函数的名称作为第一个参数，以及一个或多个关键字参数，每个参数对应于URL的变量部分。
import pymysql
import json
app = Flask(__name__)
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
        db = pymysql.connect(host=sqlconn['host'],
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
        cursor = db.cursor()
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
            db.close()
    elif request.method == 'GET':
        return render_template('sign_in.html')


# 注册方法，连接MySQL写入
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        db = pymysql.connect(host=sqlconn['host'],
                             user=sqlconn['user'],
                             password=sqlconn['password'],
                             database=sqlconn['database'])
        userId = request.form.get('Id')
        userName = request.form.get('Name')
        userPsd = request.form.get('Psd')
        userIdvalid = False
        sql = "SELECT * FROM user WHERE student_id = %s" % (userId)
        cursor = db.cursor()
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
                db.commit()
                cursor.close()
                db.close()
                return "Register success"
        # 注册成功，跳转至主页面
        # return redirect(url_for('sign_in'))
    elif request.method == 'GET':
        return render_template('sign_up.html')


@app.route('/main')
def main():
    userId = request.cookies.get('userId')
    allText = [[1, "10:00", "运动", "text"], [2, "10:00", "运动", "text"],
               [3, "10:00", "运动", "text"], [4, "10:00", "运动", "text"],
               [5, "10:00", "运动", "text"], [6, "10:00", "运动", "text"]]
    # return 'Welcome %s ,logged in successfully' % userName
    return render_template('main.html', userId=userId, allText=allText)


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