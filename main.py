import threading
import time
from flask import Flask,jsonify
from flask import request,render_template,redirect,url_for,session,g
from functions import tomlexec
from functions import smtp
from functions.time2 import hello,get_time
import sql
import sqlite3

def reset():
    db = sqlite3.connect('./lib/db/data.db')
    cur = db.cursor()
    cur.execute("UPDATE users SET ecode = ''")
    db.commit()
    cur.close()
    db.close()
    dst_file = './lib/toml/su/superadmin.toml'
    data = tomlexec.readtoml(dst_file)
    data['superadmin'][0]['emailcode'] = ''
    tomlexec.dumptoml(dst_file=dst_file, data=data)



app = Flask(__name__,static_url_path="/static")
app.config['SECRET_KEY'] = 'ks83hd7cn94'


@app.before_request
def before_request():
    sql.requestnumup()#增加记录的请求次数
    g.user = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = sql.g_readsql(keywords=user_id)[0]
        if user:
            g.user = {"id": user[0],"permissions":user[1], "username": user[2], "work":user[9]}


@app.route("/login",methods=['GET','POST'])#登录路由
def login():
    if request.method == 'POST':
        session.pop('user_id',None)
        ip_address = request.remote_addr
        if request.form.get("username",None) == tomlexec.readtomlsu()[0][0]:
            msg2 = '您无权登录该账户'
            return render_template("login.html", msg2=msg2)
        elif request.form.get('email', None) == tomlexec.readtomlsu()[0][2]:
            msg2 = '您无权登录该账户'
            return render_template("login.html", msg2=msg2)
        if request.form.get("username",None) != None:
            username = request.form.get("username",None)
            password = request.form.get("password",None)
            user = sql.readsql(table='users', keywords1=username,keywords2='username')
            if user and user[0][6] == password:
                session['user_id'] = user[0][0]
                ip_address = request.remote_addr  # ip属地
                smtp.send_verification_email_user(email=user[0][4],ip_address=ip_address)
                if user[0][1] == 2 or user[0][1] == 1:
                    return redirect(url_for('home'))
                else:
                    msg2 = "登陆权限异常，请联系管理员"
                    return render_template("login.html", msg2=msg2)
            else:
                msg1 = '用户名或密码错误'
                return render_template("login.html", msg1=msg1)

        elif request.form.get('email',None) != None:
            email = request.form.get('email',None)
            ecode = request.form.get('ecode',None)
            user = sql.readsql(table='users', keywords1=email, keywords2='email')
            msg2 = ''
            if user[0][5] == '':#未获取或验证码失效时
                code = smtp.send_verification_email(email)
                msg2 = '验证码已发送'
                sql.ecodeexec(code=code,id=user[0][0])
                return render_template("login.html", msg2=msg2)
            elif user and ecode == user[0][5]:#验证成功
                session['user_id'] = user[0][0]
                smtp.send_verification_email_user(email=user[0][4], ip_address=ip_address)
                if user[0][1]==2 or user[0][1]==1:
                    return redirect(url_for('home'))
                else:
                    msg2="登陆权限异常，请联系管理员"
                    return render_template("login.html", msg2=msg2)
            elif ecode != user[0][5]:#验证码错误
                msg2 = '验证码错误'
                return render_template("login.html", msg2=msg2)
            else:
                return render_template("login.html", msg2=msg2)
        else:
            msg1 = '用户名不能为空'
            msg2 = '邮箱不能为空'
            return render_template("login.html", msg1=msg1,msg2=msg2)
    return render_template("login.html",)


@app.route("/superlogin",methods=['GET','POST'])#登录路由
def superlogin():
    if request.method == 'POST':
        msg = '用户名或密码错误'
        session.pop('user_id',None)
        username = request.form.get("username",None)
        password = request.form.get("password",None)
        email = request.form.get("email",None)
        sid1 = request.form.get("sid1",None)
        sid2 = request.form.get("sid2",None)
        key = request.form.get("key",None)
        ecode = request.form.get("ecode",None)
        if username == None:
            msg = '用户名不能为空'
            return render_template("superlogin.html",msg=msg)
        if email == None:
            msg = '邮箱不能为空'
            return render_template("superlogin.html", msg=msg)
        users = tomlexec.readtomlsu()  # 获取超管信息
        if users[0][6] == '':
            code = smtp.send_verification_email(email)
            msg='验证码已发送'
            tomlexec.suecodeexec(code)
            return render_template("superlogin.html", msg=msg)
        quser = [username,password,email,sid1,sid2,key,ecode]
        if quser == users[0] or quser == users[1]:
            session['user_id'] = '114514'
            ip_address = request.remote_addr#ip属地
            smtp.send_verification_email_su(ip_address)
            return redirect(url_for('superhome'))
        else:
            msg = '用户名或密码错误'
            return render_template("superlogin.html",msg=msg)
    return render_template("superlogin.html")

@app.route("/signup",methods=['GET','POST'])#注册路由
def signup():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form.get('username',None)
        email = request.form.get('email',None)
        ecode = request.form.get('ecode',None)
        password1 = request.form.get('password1',None)
        password2 = request.form.get('password2', None)
        if username == '' or email == '':
            msg = '用户名和邮箱不能为空啊'
            return render_template("signup.html", msg=msg)
        if username[0] == ' ' and username[-1] == ' ':
            msg = '用户名头尾不能为空格啊'
            return render_template("signup.html", msg=msg)
        if 'qq.com' not in email:
            msg = ('暂时只支持qq.com邮箱注册')
            return render_template("signup.html", msg=msg)
        data = sql.readsql('users',username,'username')
        if data != []:
            if data[0][7] == 'enable':
                msg = '该用户名已被使用啦，可以想一个更好的啦~'
                return render_template("signup.html", msg=msg)
        email1 = sql.readsql('users',email,'email')
        if email1 != []:
            if email1[0][7] == 'enable':
                msg = '该邮箱已被注册啦'
                return render_template("signup.html", msg=msg)
        if password2 != password1:
            msg = '两次输入的密码不一样喔'
            return render_template("signup.html", msg=msg)
        id = sql.get_new_id()
        newuser = {"id":id,"permissions":2,"username":username,"phonenumber":'',"email":email,'ecode':'',"password":password2,"static":'unenable','signtime':get_time(),'work':'游客'}
        sql.sqlwrite(table='users',data=newuser)
        time.sleep(0.1)
        user = sql.readsql('users', username, 'username')
        if user[0][5] == '':
            code = smtp.send_verification_email_sign(email=email)
            msg = '验证码已发送'
            sql.ecodeexec(code=code, id=user[0][0])
            return render_template("signup.html", msg=msg)
        if ecode == user[0][5]:
            sql.sqldrop('users','username',username)
            time.sleep(0.1)
            id = sql.get_new_id()
            newuser = {"id": id, "permissions": 2, "username": username, "phonenumber": '', "email": email, 'ecode': '',"password": password2, "static": 'enable', 'signtime': get_time(),'work':'游客'}
            sql.sqlwrite(table='users',data=newuser)
            ip_address = request.remote_addr  # ip属地
            smtp.send_verification_email_user(email=newuser['email'], ip_address=ip_address)
            session['user_id'] = id
            return redirect(url_for('home'))
    return render_template("signup.html")



@app.route("/")#主路由
def home1():
    '''
    if not g.user:
        return redirect(url_for('login'))
    hellouser = f"{hello()},{g.user['username']}"
    if g.user["permissions"]==2:
        return render_template("home.html", hellouser=hellouser,message=sql.readtonggao())
    elif g.user["permissions"]==1:
        return render_template("adminhome.html", hellouser=hellouser,message=sql.readtonggao())
    elif g.user["permissions"]==3:
        return render_template("superhome.html", hellouser=hellouser,message=sql.readtonggao())
    else:
        return redirect(url_for('login'))'''
    return redirect(url_for('home'))

@app.route("/home")#主页路由
def home():
    if not g.user:
        return redirect(url_for('login'))
    hellouser = f"{hello()},{g.user['username']}"
    if g.user["permissions"] == 2:
        return render_template("home.html", hellouser=hellouser,message=sql.readtonggao())
    elif g.user["permissions"] == 3:
        return render_template("superhome.html", hellouser=hellouser, message=sql.readtonggao())
    elif g.user["permissions"] == 1:
        return render_template("adminhome.html", hellouser=hellouser, message=sql.readtonggao())
    else:
        return redirect(url_for('login'))

@app.route("/logoff")
def logoff():
    session.pop("user_id")
    return redirect(url_for('login'))

#服务条款路由
@app.route("/Terms Of Service.html")
def tos():
    return render_template("Terms Of Service.html")


#隐私权政策路由
@app.route("/Privacy Policy.html")
def pp():
    return render_template("Privacy Policy.html")


#合理使用政策路由
@app.route("/Acceptable Use Policy.html")
def AUP():
    return render_template("Acceptable Use Policy.html")

@app.route('/get_chart_data', methods=['GET'])#获取折线图数据
def get_chart_data():
    # 在实际应用中，这里应该根据你的需要从数据库或其他数据源获取数据
    data = sql.requestdata()
    chart_data = {
        'series': [{
            'name': '请求量',
            'data': data['requestnum']
        }],
        'categories': data['time']
    }
    return jsonify(chart_data)

if __name__ == "__main__":
    reset()
    app.run(debug=True)
    '''
    threads = []
    t = threading.Thread(target=sql.timethreding)
    threads.append(t)
    t = threading.Thread(target=app.run)
    threads.append(t)
    threads[0].start()
    threads[1].start()
    '''
    '''
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()'''