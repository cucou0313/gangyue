from flask import Flask, redirect, url_for, render_template, request, make_response
# url_for()函数对于动态构建特定函数的URL非常有用。该函数接受函数的名称作为第一个参数，以及一个或多个关键字参数，每个参数对应于URL的变量部分。
app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


# 登录方法，连接sqlite进行账号验证
@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        name = request.form['userName']
        password = request.form['userPsd']
        if name == 'admin' and password == 'admin':
            # 验证通过，传参并跳转至主页面
            # return redirect(url_for('main', userName=request.form['userName']))
            resp = make_response(redirect(url_for('main')))
            resp.set_cookie('userName', name)
            resp.set_cookie('userPsd', password)
            return resp
            # return redirect(url_for('main'))
        else:
            # 登录失败调回初始登录页
            return redirect(url_for('sign_in'))
    elif request.method == 'GET':
        return render_template('sign_in.html')


# 注册方法，连接sqlite写入
@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST' and request.form[
            'userName'] == 'admin' and request.form['userPsd'] == 'admin':
        # 注册成功，跳转至主页面
        return redirect(url_for('sign_in'))
    elif request.method == 'GET':
        return render_template('sign_up.html')


@app.route('/main')
def main():
    userName = request.cookies.get('userName')
    allText = [[1, "10:00", "运动", "text"], [2, "10:00", "运动", "text"],
               [3, "10:00", "运动", "text"], [4, "10:00", "运动", "text"],
               [5, "10:00", "运动", "text"], [6, "10:00", "运动", "text"]]
    # return 'Welcome %s ,logged in successfully' % userName
    return render_template('main.html', userName=userName, allText=allText)


@app.route('/user_info')
def user_info():
    userName = request.cookies.get('userName')
    userPsd = request.cookies.get('userPsd')
    return render_template('user_info.html',
                           userName=userName,
                           userPsd=userPsd)


if __name__ == '__main__':
    # 将debug = True可在debug模式中自动重启服务
    app.debug = True
    app.run(host='localhost', port=5000)