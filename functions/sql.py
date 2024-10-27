import sqlite3
import threading
import time
from time2 import get_time

def createsql():
    #try:
        db = sqlite3.connect('../lib/db/data.db')
        cur = db.cursor()
        creusers = '''CREATE TABLE IF NOT EXISTS users(
            id INT, 
            permissions INT,
            username TEXT,
            phonenumber TEXT,
            email TEXT,
            ecode TEXT,
            password TEXT,
            static TEXT,
            signtime TEXT,
            work TEXT
            )'''
        #ID,所属权限组ID,用户名,手机号,邮箱地址,邮箱验证码,密码,用户状态,创建时间,职位
        cregroups = '''CREATE TABLE IF NOT EXISTS groups(
            id INT,
            groupname TEXT
        )'''
        #用户组ID,用户组名称
        # #用户组初始设有普通用户，管理员，超级管理员三级，具体权限内容在代码中实现，详见需求文档
        credata = '''CREATE TABLE IF NOT EXISTS data(
            time TEXT,
            requestnum INT
        )'''
        #数据表，日期和请求量
        #drop = "drop table if exists mapping"
        #cur.execute(drop)
        #db.commit()
        cur.execute(creusers)
        db.commit()
        cur.execute(cregroups)
        db.commit()
        cur.execute(credata)
        db.commit()
        cur.close()
        db.close()
        print("创建成功")
    #except Exception as e:
        #print(e)

def sqlwrite(table,data):
    try:
        db = sqlite3.connect('./lib/db/data.db')
        cur = db.cursor()
        if table == 'users':
            insert = f"INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?)"
            cur.execute(insert,(data["id"],data["permissions"],data["username"],data["phonenumber"],data["email"],data['ecode'],data["password"],data["static"],data["signtime"],data['work'],))
        elif table == 'groups':
            insert = f"INSERT INTO groups VALUES(?,?)"
            cur.execute(insert,(data['id'],data['groupname']))
        elif table == 'data':
            insert = f"INSERT INTO data VALUES(?,?)"
            cur.execute(insert, (data['time'],data['requestnum']))
        db.commit()
        cur.close()
        db.close()
        print(f"{table}写入成功")
    except Exception as e:
        print(e)
def sqldrop(table,key1,key2):
    try:
        db = sqlite3.connect('./lib/db/data.db')
        cur = db.cursor()
        if table == 'users' and key1 == 'username':
            drop = 'DELETE FROM users WHERE username = ?'
            cur.execute(drop,(key2,))
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        print(e)
def sql_change_one(table, key1, key2, id):
    try:
        db = sqlite3.connect('./lib/db/data.db')
        cur = db.cursor()
        if table == 'users':
            exec = f'UPDATE users SET {key1} = ? WHERE id = ? '
            cur.execute(exec,(key2,id,))
        elif table == 'groups':
            exec = f'UPDATE groups SET {key1} = ? WHERE id = ? '
            cur.execute(exec, (key2, id,))
        elif table == 'data':
            exec = f'UPDATE data SET {key1} = ? WHERE time = ?'
            cur.execute(exec, (key2,id))
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        print(e)

def ecodeexec(code,id):
    sql_change_one(table='users', key1='ecode', key2=code, id=id)
    t = threading.Thread(target=clearecode,args=(id,))
    t.start()

def clearecode(id):
    time.sleep(60)
    sql_change_one(table='users', key1='ecode', key2='', id=id)


def readsql(table,keywords1,keywords2):
    db = sqlite3.connect('./lib/db/data.db')
    cur = db.cursor()
    if table == 'users' and keywords2 == 'username':
        read = "SELECT * FROM users WHERE username = ?"
        cur.execute(read,(keywords1,))
    elif table == 'users' and keywords2 == 'email':
        read = "SELECT * FROM users WHERE email = ?"
        cur.execute(read, (keywords1, ))
    elif table == 'users' and keywords2 == '*':
        read = "SELECT * FROM users"
        cur.execute(read)
    elif table == 'groups':
        read = f"SELECT * FROM groups WHERE id = ?"
        cur.execute(read,(keywords1,))
    db.commit()
    data = cur.fetchall()
    cur.close()
    db.close()
    return data

def g_readsql(keywords):
    db = sqlite3.connect('./lib/db/data.db')
    cur = db.cursor()
    read = f"SELECT * FROM users WHERE id = ?"
    cur.execute(read,(keywords,))
    db.commit()
    data = cur.fetchall()
    cur.close()
    db.close()
    return data
def get_new_id():
    db = sqlite3.connect('./lib/db/data.db')
    cur = db.cursor()
    cur.execute('SELECT id FROM users')
    data = cur.fetchall()
    id = str(int(data[-1][0])+1)
    cur.close()
    db.close()
    return id

def requestnumup():
    db = sqlite3.connect('./lib/db/data.db')
    cur = db.cursor()
    cur.execute(f'SELECT requestnum FROM data WHERE time = ?',(get_time()[0:10],))
    if cur.fetchall() == []:
        insert = f"INSERT INTO data VALUES(?,?)"
        cur.execute(insert, (get_time()[0:10], 0))
        db.commit()
    cur.execute(f'SELECT requestnum FROM data WHERE time = ?', (get_time()[0:10],))
    data = cur.fetchall()[0][0]+1
    sql_change_one('data', 'requestnum', data, get_time()[0:10])
    cur.close()
    db.close()
    return data

def requestdata():
    db = sqlite3.connect('./lib/db/data.db')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM data')
    data = cur.fetchall()
    out = {'time':[],'requestnum':[]}
    for i in data[-9:]:
        out['time'].append(i[0])
        out['requestnum'].append(i[1])
    cur.close()
    db.close()
    return out

def readtonggao():
    # 打开文件
    with open('./lib/txt/通告.txt', 'r', encoding='utf-8') as file:
        tonggao = file.read()
    return tonggao



if __name__ == "__main__":
    '''
    #readtonggao()
    #print(readsql('users','bayue','username'))

    #requestnumup()
    #sqldrop('users','username','bayuetest')
    '''
    createsql()
    #data1 = {"id":114514,"permissions":3,"username":'bayue',"phonenumber":'13185098816',"email":'2676796446@qq.com',"ecode":'',"password":'bznaipyc1314',"static":'enable','signtime':get_time(),'work':'大股东,机房运维,售前售后'}
    data2 = {"id":2,"permissions":1,"username":'jiuxia2025',"phonenumber":'13397659420',"email":'2025226181@qq.com','ecode':'',"password":'123456',"static":'enable','signtime':get_time(),'work':'股东,技术顾问,运维，售前售后'}
    #data3 = {"id":3, "permissions": 2, "username": 'test', "phonenumber": '19817102129', "email": '2676796446@qq.com','ecode':'',"password": '123456', "static": 'enable','signtime':get_time(),'work':'测试账户，无职位'}
    data4 = {'id':1,'groupname':'admin'}
    data5 = {'id':2, 'groupname': 'user'}
    data6 = {'id': 1, "permissions": 1, "username": 'horon', "phonenumber": '15158010653', "email": '3205447513@qq.com',"ecode": '', "password": '123456', "static": 'enable', 'signtime': get_time(),'work':'股东,技术,运维,售前售后'}
    data7 = {'id':3, 'groupname': 'superadmin'}

    #sqlwrite("users", data1)
    sqlwrite('users', data6)
    sqlwrite("users", data2)
    #sqlwrite("users", data3)

    sqlwrite('groups',data4)
    sqlwrite('groups',data5)
    sqlwrite('groups',data7)
    
    j = -1
    num = [302,519,476,201,304,122,277,89,320]
    for i in ['2024-01-16','2024-01-17','2024-01-18','2024-01-19','2024-01-20','2024-01-21','2024-01-22','2024-01-29','2024-01-30']:
        j+=1
        data8 = {'time': i, 'requestnum': num[j]}
        sqlwrite( 'data', data8)