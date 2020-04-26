import pymysql
import time

sqlconn = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'gangyue'
}

pymysql_db = pymysql.connect(host=sqlconn['host'],
                             user=sqlconn['user'],
                             password=sqlconn['password'],
                             database=sqlconn['database'])

def sign_in(studentId, password):
    cursor = pymysql_db.cursor()
    sql = "SELECT id, student_id, name FROM user WHERE student_id = %s and password = '%s'" % (
        studentId, password)
    result = {}
    result['success'] = 0
    result['data'] = ()
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            sqlData = cursor.fetchone()
            result['data'] = sqlData
            return result
        else:
            result['errorMessage'] = "User info error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        cursor.close()

def sign_up(studentId, name, password):
    cursor = pymysql_db.cursor()
    sql = "SELECT * FROM user WHERE student_id = %s" % (studentId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        if success:
            result['success'] = 0
            result['errorMessage'] = "The user is already registered"
            return result
        else:
            sql = "INSERT INTO user (student_id, name, password, is_active) VALUES ( %s, '%s', '%s', 1);" % (
                studentId, name, password)
            success = cursor.execute(sql)
            result['success'] = success
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        pymysql_db.commit()
        cursor.close()

def get_post(postId):
    cursor = pymysql_db.cursor()
    sql = "SELECT * FROM post WHERE id=%s;" % (postId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    result['data'] = ()
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            sqlData = cursor.fetchone()
            result['data'] = sqlData
            return result
        else:
            result['errorMessage'] = "Get post error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        cursor.close()

def get_posts(number, isActive=None, isKnot=None):
    cursor = pymysql_db.cursor()
    sql = "SELECT * FROM post "
    if isActive!=None:
        if isKnot!=None:
            sql+="WHERE is_active=%s AND is_knot=%s " % (isActive, isKnot)
        else:
            sql+="WHERE is_active=%s " % (isActive)
    elif isKnot!=None:
        sql+="WHERE is_knot=%s " % (isKnot)
    sql+="ORDER BY added_time DESC LIMIT %s;" % (number)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    result['data'] = ()
    try:
        success = cursor.execute(sql)
        result['number'] = success
        if success:
            result['success'] = 1
            sqlData = cursor.fetchall()
            result['data'] = sqlData
            return result
        else:
            result['errorMessage'] = "Get posts error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        cursor.close()

def get_user(userId):
    cursor = pymysql_db.cursor()
    sql = "SELECT student_id, name FROM user WHERE id=%s;" % (userId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    result['data'] = ()
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            sqlData = cursor.fetchone()
            result['data'] = sqlData
            return result
        else:
            result['errorMessage'] = "Get user error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        cursor.close()

def get_reply(postId):
    cursor = pymysql_db.cursor()
    sql = "SELECT * FROM reply WHERE post_id=%s ORDER BY added_time;" % (postId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    result['data'] = ()
    try:
        success = cursor.execute(sql)
        result['number'] = success
        if success:
            result['success'] = 1
            sqlData = cursor.fetchall()
            result['data'] = sqlData
            return result
        else:
            result['errorMessage'] = "Get reply error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        cursor.close()

def add_post(userId, title, category):
    cursor = pymysql_db.cursor()
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    sql = "insert into post(title, category, added_time, user_id, is_active, is_knot) " \
          "values ('%s', '%s', '%s', %s, 1, 0);" % (title, category, currentTime, userId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            return result
        else:
            result['errorMessage'] = "Add post error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        pymysql_db.commit()
        cursor.close()

def add_reply(userId, postId, content):
    cursor = pymysql_db.cursor()
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    sql = "insert into reply(content, added_time, post_id, user_id) " \
          "values ('%s', '%s', '%s', %s);" % (content, currentTime, postId, userId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            return result
        else:
            result['errorMessage'] = "Add reply error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        pymysql_db.commit()
        cursor.close()

def get_user_post(userId):
    cursor = pymysql_db.cursor()
    sql = "select * from post where user_id=%s order by added_time desc;" % (userId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['number'] = success
        if success:
            result['success'] = 1
            sqlData = cursor.fetchall()
            result['data'] = sqlData
            return result
        else:
            result['errorMessage'] = "Get user post error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        cursor.close()

def get_user_reply(userId):
    cursor = pymysql_db.cursor()
    sql = "select * from reply where user_id=%s order by added_time desc;" % (userId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['number'] = success
        if success:
            result['success'] = 1
            sqlData = cursor.fetchall()
            result['data'] = sqlData
            return result
        else:
            result['errorMessage'] = "Get user reply error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        cursor.close()

def change_password(userId, password):
    cursor = pymysql_db.cursor()
    sql = "UPDATE user SET password='%s' WHERE id=%s;" % (password, userId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            return result
        else:
            result['errorMessage'] = "Change password error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        pymysql_db.commit()
        cursor.close()

def delete_post(postId):
    cursor = pymysql_db.cursor()
    sql = "UPDATE post SET is_active=0 WHERE id=%s;" % (postId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            return result
        else:
            result['errorMessage'] = "delete post error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        pymysql_db.commit()
        cursor.close()

def knot_post(postId):
    cursor = pymysql_db.cursor()
    sql = "UPDATE post SET is_knot=1 WHERE id=%s;" % (postId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            return result
        else:
            result['errorMessage'] = "knot post error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        pymysql_db.commit()
        cursor.close()

def delete_user(userId):
    cursor = pymysql_db.cursor()
    sql = "UPDATE user SET is_active=0 WHERE id=%s;" % (userId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            return result
        else:
            result['errorMessage'] = "delete user error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        pymysql_db.commit()
        cursor.close()

def delete_reply(replyId):
    cursor = pymysql_db.cursor()
    sql = "DELETE FROM reply WHERE id=%s;" % (replyId)
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    try:
        success = cursor.execute(sql)
        result['success'] = success
        if success:
            return result
        else:
            result['errorMessage'] = "delete reply error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        pymysql_db.commit()
        cursor.close()

def search_post_by_category(category, isActive=None, isKnot=None):
    cursor = pymysql_db.cursor()
    sql = "SELECT * FROM post WHERE category='%s' " % (category)
    if isActive != None:
        sql += "AND is_active=%s " % (isActive)
    if isKnot != None:
        sql += "AND is_knot=%s " % (isKnot)
    sql += "ORDER BY added_time DESC;"
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    result['data'] = ()
    try:
        success = cursor.execute(sql)
        result['number'] = success
        if success:
            result['success'] = 1
            sqlData = cursor.fetchall()
            result['data'] = sqlData
            return result
        else:
            result['errorMessage'] = "Search post by category error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        cursor.close()

def search_post_by_title(title, isActive=None, isKnot=None):
    cursor = pymysql_db.cursor()
    sql = "SELECT * FROM post WHERE title LIKE '%%%s%%' " % (title)
    if isActive != None:
        sql += "AND is_active=%s " % (isActive)
    if isKnot != None:
        sql += "AND is_knot=%s " % (isKnot)
    sql += "ORDER BY added_time DESC;"
    result = {}
    result['success'] = 0
    result['errorMessage'] = ""
    result['data'] = ()
    try:
        success = cursor.execute(sql)
        result['number'] = success
        if success:
            result['success'] = 1
            sqlData = cursor.fetchall()
            result['data'] = sqlData
            return result
        else:
            result['errorMessage'] = "Search post by title error"
            return result
    except Exception as e:
        print(e)
        result['errorMessage'] = "An unknown error has happened"
        return result
    finally:
        cursor.close()
