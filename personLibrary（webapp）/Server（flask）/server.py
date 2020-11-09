import datetime
import hashlib
import json
import random
import sys,os,base64,hmac
from datetime import date, datetime

import mysql
import pymysql
from flask import Flask, escape, request, session
from flask_cors import CORS
import redis
import config
#引用阿里云短信模块
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
app=Flask(__name__)
cors = CORS(app)
conn=pymysql.Connect(database='mysql_python',
        host='localhost',
        user='root',
        password='root',
        port=3306)
userdata={}
@app.route("/")
def index():
    return "{a:1,b:2}"

#账号密码登录
@app.route("/user/login",methods=["POST"])
def login():
    #获取用户名和密码
    name=request.json.get("name")
    phone=request.json.get("phone")
    password=request.json.get("password")
    returnmsg = {"status":0,"desc":"登录成功","uid":1}
    #加密了密码
    password=hashlib.sha1(password.encode()).hexdigest()
    #数据库查询数据
    result=mysql.doIt("SELECT wusername,wuserid,wuserimage,wuserinsert_time,wuserphone,walimit from wuser WHERE wusername='"+name+"' or wuserphone='"+phone+"'")
    if len(result)==0:
        returnmsg["status"]=1
        returnmsg["desc"]="登陆失败,请注册后重试"
        returnmsg["uid"]=0
    else:
        nu_result=mysql.doIt("SELECT wusername,wuserid,wuserimage,wuserinsert_time,wuserphone,walimit from wuser WHERE wusername='"+name+"' and wuserpassword='"+password+"'" )
        np_result=mysql.doIt("SELECT wusername,wuserid,wuserimage,wuserinsert_time,wuserphone,walimit from wuser WHERE wuserphone='"+phone+"' and wuserpassword='"+password+"'")
        # print(nu_result)
        # print(np_result)
        if len(nu_result)==0:
            if len(np_result)==0:
                returnmsg["status"]=1
                returnmsg["desc"]="密码错误,请重新再试"
                returnmsg["uid"]=0
            else:
                returnmsg["desc"]="欢迎你," + result[0]["wusername"]
                returnmsg["info"]=result[0]
        else:
            returnmsg["desc"]="欢迎你," + result[0]["wusername"]
            returnmsg["info"]=result[0]

    return json.dumps(returnmsg,cls=CJsonEncoder)

@app.route("/user/codelogin",methods=["POST"])
def codelogin():
    phone=request.json.get("phone")
    msg={"status":0,"desc":"获取成功"}
    now_time=datetime.now()
    send_time=now_time.strftime('%Y-%m-%d %H:%M:%S')
    code_res=mysql.doIt("SELECT code_id from user_code WHERE phone='"+phone+"'")
    user_im=mysql.doIt("SELECT wusername,wuserid,wuserimage,wuserinsert_time,wuserphone,walimit from wuser WHERE wuserphone='"+phone+"'")
    if len(user_im)==0:
        msg["status"]=1
        msg["desc"]="未注册,请先进行注册"
    
    else:
        isnew=0
        if len(code_res)!=0:
            isnew=code_res[0]
    #向阿里发起短信请求
        client = AcsClient('LTAI4GDwZHYSscp2kmD8ywQD', '862r2ip3EQ04VngYRYykBj3XCB8Jor', 'cn-hangzhou')
        reqs = CommonRequest()
        reqs.set_accept_format('json')
        reqs.set_domain('dysmsapi.aliyuncs.com')
        reqs.set_method('POST')
        reqs.set_protocol_type('https') # https | http
        reqs.set_version('2017-05-25')
        reqs.set_action_name('SendSms')

        reqs.add_query_param('RegionId', "cn-hangzhou")
        reqs.add_query_param('PhoneNumbers', phone)
        reqs.add_query_param('SignName', "书香年华")
        reqs.add_query_param('TemplateCode', "SMS_189763364")
        number=random.randint(10000,99999)
        number=str(number)
        reqs.add_query_param('TemplateParam', "{\"code\":\""+number+"\"}")
        #SMS_189763364
        ress = client.do_action(reqs)
        if isnew==0:
            mysql.Excuit("INSERT INTO user_code (phone,code,send_time) VALUES ('"+str(phone)+"','"+number+"','"+send_time+"') ")
        else:
            mysql.Excuit("UPDATE user_code SET code ='"+number+"',send_time='"+send_time+"' where phone='"+str(phone)+"'")
        msg["code"]=number
    return json.dumps(msg,cls=CJsonEncoder)

@app.route("/user/phone_code_yz",methods=["POST"])
def code_phone_login():
    phone=request.json.get("phone")
    msg={"status":0,"desc":"获取成功"}
    now_time=datetime.now()
    send_time=now_time.strftime('%Y-%m-%d %H:%M:%S')
    code_res=mysql.doIt("SELECT code_id from user_code WHERE phone='"+phone+"'")
    user_im=mysql.doIt("SELECT wusername,wuserid,wuserimage,wuserinsert_time,wuserphone,walimit from wuser WHERE wuserphone='"+phone+"'")
    if len(user_im)==0:
        msg["status"]=1
        msg["desc"]="未注册,请先进行注册"
    
    else:
        isnew=0
        if len(code_res)!=0:
            isnew=code_res[0]
    #向阿里发起短信请求
        client = AcsClient('LTAI4GDwZHYSscp2kmD8ywQD', '862r2ip3EQ04VngYRYykBj3XCB8Jor', 'cn-hangzhou')
        reqs = CommonRequest()
        reqs.set_accept_format('json')
        reqs.set_domain('dysmsapi.aliyuncs.com')
        reqs.set_method('POST')
        reqs.set_protocol_type('https') # https | http
        reqs.set_version('2017-05-25')
        reqs.set_action_name('SendSms')

        reqs.add_query_param('RegionId', "cn-hangzhou")
        reqs.add_query_param('PhoneNumbers', phone)
        reqs.add_query_param('SignName', "书香年华")
        reqs.add_query_param('TemplateCode', "SMS_189763365")
        number=random.randint(10000,99999)
        number=str(number)
        reqs.add_query_param('TemplateParam', "{\"code\":\""+number+"\"}")
        #SMS_189763364
        ress = client.do_action(reqs)
        if isnew==0:
            mysql.Excuit("INSERT INTO user_code (phone,code,send_time) VALUES ('"+str(phone)+"','"+number+"','"+send_time+"') ")
        else:
            mysql.Excuit("UPDATE user_code SET code ='"+number+"',send_time='"+send_time+"' where phone='"+str(phone)+"'")
        msg["code"]=number
    return json.dumps(msg,cls=CJsonEncoder)

@app.route("/user/phone_zhuce",methods=["POST"])
def code_phone_zhuce():
    phone=request.json.get("phone")
    msg={"status":0,"desc":"获取成功"}
    now_time=datetime.now()
    send_time=now_time.strftime('%Y-%m-%d %H:%M:%S')
    code_res=mysql.doIt("SELECT code_id from user_code WHERE phone='"+phone+"'")
    user_im=mysql.doIt("SELECT wusername,wuserid,wuserimage,wuserinsert_time,wuserphone,walimit from wuser WHERE wuserphone='"+phone+"'")
    if len(user_im)!=0:
        msg["status"]=1
        msg["desc"]="已注册,请直接登录"
    
    else:
        isnew=0
        if len(code_res)!=0:
            isnew=code_res[0]
    #向阿里发起短信请求
        client = AcsClient('LTAI4GDwZHYSscp2kmD8ywQD', '862r2ip3EQ04VngYRYykBj3XCB8Jor', 'cn-hangzhou')
        reqs = CommonRequest()
        reqs.set_accept_format('json')
        reqs.set_domain('dysmsapi.aliyuncs.com')
        reqs.set_method('POST')
        reqs.set_protocol_type('https') # https | http
        reqs.set_version('2017-05-25')
        reqs.set_action_name('SendSms')

        reqs.add_query_param('RegionId', "cn-hangzhou")
        reqs.add_query_param('PhoneNumbers', phone)
        reqs.add_query_param('SignName', "书香年华")
        reqs.add_query_param('TemplateCode', "SMS_189763356")
        number=random.randint(10000,99999)
        number=str(number)
        reqs.add_query_param('TemplateParam', "{\"code\":\""+number+"\"}")
        #SMS_189763364
        ress = client.do_action(reqs)
        if isnew==0:
            mysql.Excuit("INSERT INTO user_code (phone,code,send_time) VALUES ('"+str(phone)+"','"+number+"','"+send_time+"') ")
        else:
            mysql.Excuit("UPDATE user_code SET code ='"+number+"',send_time='"+send_time+"' where phone='"+str(phone)+"'")
        msg["code"]=number
    return json.dumps(msg,cls=CJsonEncoder)

@app.route("/user/phone_change",methods=["POST"])
def code_phone_change():
    phone=request.json.get("phone")
    msg={"status":0,"desc":"获取成功"}
    now_time=datetime.now()
    send_time=now_time.strftime('%Y-%m-%d %H:%M:%S')
    code_res=mysql.doIt("SELECT code_id from user_code WHERE phone='"+phone+"'")
    user_im=mysql.doIt("SELECT wusername,wuserid,wuserimage,wuserinsert_time,wuserphone,walimit from wuser WHERE wuserphone='"+phone+"'")
    if len(user_im)==0:
        msg["status"]=1
        msg["desc"]="系统繁忙"
    
    else:
        isnew=0
        if len(code_res)!=0:
            isnew=code_res[0]
    #向阿里发起短信请求
        client = AcsClient('LTAI4GDwZHYSscp2kmD8ywQD', '862r2ip3EQ04VngYRYykBj3XCB8Jor', 'cn-hangzhou')
        reqs = CommonRequest()
        reqs.set_accept_format('json')
        reqs.set_domain('dysmsapi.aliyuncs.com')
        reqs.set_method('POST')
        reqs.set_protocol_type('https') # https | http
        reqs.set_version('2017-05-25')
        reqs.set_action_name('SendSms')

        reqs.add_query_param('RegionId', "cn-hangzhou")
        reqs.add_query_param('PhoneNumbers', phone)
        reqs.add_query_param('SignName', "书香年华")
        reqs.add_query_param('TemplateCode', "SMS_189763356")
        number=random.randint(10000,99999)
        number=str(number)
        reqs.add_query_param('TemplateParam', "{\"code\":\""+number+"\"}")
        #SMS_189763364
        ress = client.do_action(reqs)
        if isnew==0:
            mysql.Excuit("INSERT INTO user_code (phone,code,send_time) VALUES ('"+str(phone)+"','"+number+"','"+send_time+"') ")
        else:
            mysql.Excuit("UPDATE user_code SET code ='"+number+"',send_time='"+send_time+"' where phone='"+str(phone)+"'")
        msg["code"]=number
    return json.dumps(msg,cls=CJsonEncoder)

@app.route("/user/bdwp",methods=["POST"])
def bindlimit():
    phone=request.json.get("phone")
    code=request.json.get("code")
    msg={"status":0,"desc":"修改成功"}
    res_code=mysql.doIt("select *from user_code where phone='"+str(phone)+"' and code='"+str(code)+"'")
    if len(res_code)==0:
        msg["status"]=1
        msg["desc"]="验证码输入错误"

    else:
        mysql.Excuit("update wuser SET walimit='"+str(99)+"' where wuserphone='"+phone+"'")
        user_im=mysql.doIt("SELECT wusername,wuserid,wuserimage,wuserinsert_time,wuserphone,walimit from wuser where wuserphone='"+phone+"'")
        msg["info"]=user_im[0]

    return json.dumps(msg,cls=CJsonEncoder)
@app.route("/user/yzmlogin",methods=["POST"])
def yzmlogin():
    phone=request.json.get("phone")
    code=request.json.get("code")
    msg={"status":0,"desc":"登录成功"}
    res_code=mysql.doIt("select *from user_code where phone='"+str(phone)+"' and code='"+str(code)+"'")
    if len(res_code)==0:
        msg["status"]=1
        msg["desc"]="验证码输入错误"

    else:
        user_im=mysql.doIt("SELECT wusername,wuserid,wuserimage,wuserinsert_time,wuserphone,walimit from wuser where wuserphone='"+phone+"'")
        msg["info"]=user_im[0]
    
    return json.dumps(msg,cls=CJsonEncoder)

@app.route("/code/rm",methods=["POST"])
def rmcode():
    msg={"status":"null","desc":"null"}
    phone=request.json.get("phone")
    now_time=datetime.now()
    number=random.randint(10000000,99999999)
    number=str(number)
    send_time=now_time.strftime('%Y-%m-%d %H:%M:%S')
    mysql.Excuit("UPDATE user_code SET code ='"+number+"',send_time='"+send_time+"' where phone='"+str(phone)+"'")
    return json.dumps(msg,cls=CJsonEncoder)

@app.route("/user/zhuce",methods=["POST"])
def zhuce():
    thistime=datetime.now()
    returnmsg = {"status":0,"desc":"注册成功","uid":1}
    #接收数据
    name=request.json.get("username")
    phone=request.json.get("userphone")
    password=request.json.get("userpassword")
    code=request.json.get("code")
    limit=str(9)
    password=hashlib.sha1(password.encode()).hexdigest()
    #数据库查询用户信息是否存在
    userid='2'
    it=[random.randint(0,9) for _ in range(6)]
    for each in it:
        userid=userid+str(each)
    it_res=mysql.doIt("SELECT wuserid,wusername,wuserphone from wuser where wuserid='"+userid+"'")
    while len(it_res)!=0:
        userid='2'
        it=[random.randint(0,9) for _ in range(6)]
        for each in it:
            userid=userid+str(each)
        it_res=mysql.doIt("SELECT wuserid,wusername,wuserphone from wuser where wuserid='"+userid+"'")
    cursor= conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT wuserid,wusername,wuserphone from wuser where wuserphone='"+phone+"' or wusername='"+name+"'")
    result = cursor.fetchall()
    un=mysql.doIt("SELECT wuserid,wusername,wuserphone from wuser where wusername='"+name+"'")
    up=mysql.doIt("SELECT wuserid,wusername,wuserphone from wuser where wuserphone='"+phone+"'")
    if len(result)==0:
        res_code=mysql.doIt("select *from user_code where phone='"+str(phone)+"' and code='"+str(code)+"'")
        if len(res_code)==0:
            returnmsg["status"]=2
            returnmsg["desc"]="验证码错误,请重新输入"
        else:
            mysql.Excuit('INSERT INTO wuser (wuserid,wuserphone,wusername,wuserinsert_time,wuserpassword,walimit) VALUES("'+userid+'","'+phone+'","'+name+'","'+thistime.strftime('%Y-%m-%d %H:%M:%S')+'","'+password+'","'+limit+'");')
            result_1=mysql.doIt("SELECT wuserid,wusername,wuserphone from wuser where wuserphone='"+phone+"' or wusername='"+name+"';")
            if len(result_1)==0:
            #插入失败
                returnmsg["status"]=1
                returnmsg["desc"]="系统繁忙,请稍后再试"
            else:
               #插入成功
                returnmsg["desc"]="注册成功,请使用该账号进行登录"
                returnmsg["info"]=result_1[0]
    else:
        if len(un)!=0:
            if len(up)!=0:
                returnmsg["status"]=1
                returnmsg["desc"]="操作失败,您已注册"
                returnmsg["uid"]=0
            else:
                returnmsg["status"]=1
                returnmsg["desc"]="操作失败,用户名已被注册"
                returnmsg["uid"]=0
        else:
            if len(up)!=0:
                returnmsg["status"]=1
                returnmsg["desc"]="操作失败,手机号已被注册"
                returnmsg["uid"]=0
            
    #存在用户信息,返回登陆提示

    return json.dumps(returnmsg,cls=CJsonEncoder)

@app.route("/user/gerenxinxi",methods=["POST"])
def get_user_im():
    userid=request.json.get("userid")
    msg = {"status":0,"desc":"显示成功"}
    result=mysql.getone("SELECT *FROM wuser WHERE wuserid="+str(userid))
    if result!=None:
        msg["data"]=result

    return json.dumps(msg,cls=CJsonEncoder)

@app.route("/user/changeim",methods=["POST"])
def changeuser():
    msg = {"status":0,"desc":"显示成功"}
    userid=request.json.get("userid")
    username=request.json.get("username")
    userphone=request.json.get("userphone")
    password=request.json.get("userpassword")
    password=hashlib.sha1(password.encode()).hexdigest()
    result=mysql.getone("SELECT *FROM wuser where wuserid="+str(userid))
    name_1=result["wusername"]
    other_result=mysql.getone("SELECT *FROM wuser where wusername='"+username+"'")
    if name_1==username:
        if userphone==result["wuserphone"]:
            if password==result["wuserpassword"]:
                msg["desc"]="未更换信息,请重试"
                msg["status"]=1
            else:
                mysql.Excuit("UPDATE wuser SET wuserpassword='"+password+"' where wuserid='"+str(userid)+"'")
                msg["desc"]="密码修改成功,请使用新用户名和密码登录"
        else:
            if password==result["wuserpassword"]:
                mysql.Excuit("UPDATE wuser SET wuserphone='"+userphone+" where wuserid='"+str(userid)+"'")
                msg["desc"]="手机号修改成功"
            else:
                mysql.Excuit("UPDATE wuser SET wuserphone='"+userphone+"',wuserpassword='"+password+"' where wuserid='"+str(userid)+"'")
                msg["desc"]="手机号和密码修改成功,请使用新用户名和密码登录"
    else:
        if other_result!=None:
            msg["desc"]="与其他用户的用户名相同,请更换后重试"
            msg["status"]=1
        else:
            if userphone==result["wuserphone"]:
                if password==result["wuserpassword"]:
                     mysql.Excuit("UPDATE wuser SET wusername='"+username+"' where wuserid='"+str(userid)+"'")
                     msg["desc"]="用户名修改成功"
                else:
                    mysql.Excuit("UPDATE wuser SET wusername='"+username+"',wuserpassword='"+password+"' where wuserid='"+str(userid)+"'")
                    msg["desc"]="用户名和密码修改成功"
            else:
                if password==result["wuserpassword"]:
                    mysql.Excuit("UPDATE wuser SET wusername='"+username+"',wuserphone='"+userphone+"' where wuserid='"+str(userid)+"'")
                    msg["desc"]="用户名和手机号修改成功"
                    
                else:
                    mysql.Excuit("UPDATE wuser SET wusername='"+username+"',wuserphone='"+userphone+"',wuserpassword='"+password+"' where wuserid='"+str(userid)+"'")
                    msg["desc"]="修改成功,请使用新用户名和密码登录"
    
    return json.dumps(msg,cls=CJsonEncoder)
                
@app.route("/user/types")
def get_types():
    #查询分类
    types = mysql.doIt("select wyid,wyname from wcategory order by wyid;")

    #查询分类下所有书籍
    result = mysql.doIt("select *from book;")

    for p in types:
        p["data"]=[one for one in result if one["wyid"]==p["wyid"]]

    return json.dumps(types,cls=CJsonEncoder)

@app.route("/book/detail")
def get_bookdetail():
    id=request.args.get("id")
    detail=mysql.getone("SELECT *FROM book WHERE wbookid="+str(id))
    category=detail["wyid"]
    rcategory=mysql.getone("SELECT *FROM wcategory WHERE wyid='"+str(category)+"'")
    returnmsg={"detail":detail,"rcategory":rcategory}
    return returnmsg

@app.route("/card/invitate")
def get_invitate():
    invitate=mysql.doIt("SELECT *FROM invitation;")
    changdu=len(invitate)
    returnmsg={"invatate":invitate,"changdu":changdu}
    return json.dumps(returnmsg,cls=CJsonEncoder)

@app.route("/index/banner")
def get_random_book():
    one=str(random.randint(743,842))
    two=str(random.randint(643,742))
    three=str(random.randint(343,642))
    four=str(random.randint(143,342))
    five=str(random.randint(0,142))
    banner_1=mysql.getone("SELECT *FROM book WHERE wbookid='"+one+"';")
    banner_2=mysql.getone("SELECT *FROM book WHERE wbookid='"+two+"';")
    banner_3=mysql.getone("SELECT *FROM book WHERE wbookid='"+three+"';")
    banner_4=mysql.getone("SELECT *FROM book WHERE wbookid='"+four+"';")
    banner_5=mysql.getone("SELECT *FROM book WHERE wbookid='"+five+"';")
    banner={"banner_1":banner_1,"banner_2":banner_2,"banner_3":banner_3,"banner_4":banner_4,"banner_5":banner_5}
    return json.dumps(banner,cls=CJsonEncoder)

@app.route("/index/search",methods=["POST"])
def get_search():
    search_book=request.json.get("search")
    lensearch_book=len(search_book)
    search_result={"status":1,"desc":"没有找到该书籍,请重新搜索","uid":0}
    if lensearch_book==0:
        search_result["desc"]="输入为空,请重新输入"
    else:
        result=mysql.doIt("SELECT * FROM book WHERE wbookname LIKE '%"+search_book+"%' OR wbookauthor LIKE '%"+search_book+"%'")
        len_search=str(len(result))
        if result!=0:
            search_result["status"]=0
            search_result["desc"]="共找到'"+len_search+"'本书籍"
            search_result["uid"]=1
            search_result["data"]=result
    
    
    return json.dumps(search_result,cls=CJsonEncoder)

@app.route("/my/like",methods=["POST"])
def add_like():
    username=request.json.get("username")
    bookname=request.json.get("bookname")
    add_result={"status":1,"desc":"加入失败,你已收藏该书","uid":0}
    result= mysql.getone("SELECT *FROM wfavious WHERE wusername ='"+username+"' AND wbookname='"+bookname+"'")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if result==None:
        cursor.execute('INSERT INTO wfavious (wusername,wbookname) VALUES("'+username+'","'+bookname+'")')
        add_result["status"]=0
        add_result["desc"]="添加成功"
        add_result["uid"]=1
    
    cursor.connection.commit()
    
    return json.dumps(add_result,cls=CJsonEncoder)

@app.route("/my/mylike",methods=["POST"])
def my_like():
    like_username=request.json.get("username")
    like_result={"status":1,"desc":"你还未收藏书籍,快去收藏一本吧!","uid":0}
    book_result = mysql.doIt("select *from book;")
    result=mysql.doIt("SELECT *FROM wfavious WHERE wusername='"+like_username+"'")
    if result!=None:
        for p in result:
            p["data"]=[one for one in book_result if one["wbookname"]==p["wbookname"]]
        
        like_result["status"] =0
        like_result["desc"]=""
        like_result["uid"]=1
        like_result["like"]=result
    
    return json.dumps(like_result,cls=CJsonEncoder)

@app.route("/goods/chaxun",methods=["POST"])
def get_chaxun_result():
    like_username=request.json.get("username")
    like_bookname=request.json.get("bookname")
    chaxun_result={"status":1,"desc":"此书你已收藏,去看看其他书吧","uid":0}
    result=mysql.getone("SELECT *FROM wfavious WHERE wusername ='"+like_username+"' AND wbookname='"+like_bookname+"'")
    if result==None:
        chaxun_result["status"]=0
        chaxun_result["desc"]=""
        chaxun_result["uid"]=1
    return json.dumps(chaxun_result,cls=CJsonEncoder)
    
@app.route("/mylike/remove",methods=["POST"])
def remove_like():
    rv_username=request.json.get("username")
    rv_bookname=request.json.get("bookname")
    print(rv_username)
    print(rv_bookname)
    remove_im={"status":1,"desc":"删除失败","uid":0}
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM wfavious WHERE wusername='"+rv_username+"' AND wbookname='"+rv_bookname+"'")
    cursor.connection.commit()
    result=mysql.getone("SELECT *FROM wfavious WHERE wusername='"+rv_username+"' AND wbookname='"+rv_bookname+"'")
    if result==None:
        remove_im["status"]=0
        remove_im["desc"]="该书已从你的收藏夹删除!"
        remove_im["uid"]=1
    else:
        remove_im["desc"]="操作取消"
    return json.dumps(remove_im,cls=CJsonEncoder)

@app.route("/admin/adminlogin",methods=["POST"])
def getadmin_login():
    msg={"status":0,"desc":"登录成功"}
    phone=request.json.get("phone")
    password=request.json.get("password")
    password=hashlib.sha1(password.encode()).hexdigest()
    up=mysql.doIt("select *from adminuser where wadminphone='"+str(phone)+"' and wapassword='"+password+"'")
    un=mysql.doIt("select *from adminuser where wadminname='"+str(phone)+"' and wapassword='"+password+"'")
    if len(up)==0:
        if len(un)==0:
            msg["status"]=1
            msg["desc"]="账户或密码不正确"
        else:
            msg["desc"]="欢迎回来"
            msg["data"]=un[0]
        
    else:
        msg["desc"]="欢迎回来"
        msg["data"]=up[0]
    return json.dumps(msg,cls=CJsonEncoder)


@app.route("/admin/getmy",methods=["POST"])
def get_admin_my():
    phone=request.json.get("phone")
    msg={"status":1,"desc":"获取失败"}
    up=mysql.doIt("select *from adminuser where wadminphone='"+str(phone)+"'")
    un=mysql.doIt("select *from adminuser where wadminname='"+str(phone)+"'")
    adnp=mysql.doIt("select *from wuser where wuserphone='"+str(phone)+"'")
    if len(up)==0:
        if len(un)==0:
            msg["desc"]="账号密码不正确"
        else:
            adnu=mysql.doIt("select *from wuser where wuserphone='"+str(un[0]["wadminphone"])+"'")
            if len(adnu)==0:
                msg["desc"]="暂无用户角色"
            else:
                msg["data"]=un[0]
                msg["status"]=0
                msg["info"]=adnu[0]
        
    else:
        if len(adnp)==0:
            msg["desc"]="暂无用户角色"
        else:
            msg["data"]=up[0]
            msg["status"]=0
            msg["info"]=adnp[0]
    
    return json.dumps(msg,cls=CJsonEncoder)

@app.route("/mylike/delete",methods=["POST"])
def admin_remove_like():
    rv_bookname=request.json.get("bookname")
    remove_im={"status":1,"desc":"删除失败","uid":0}
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM wfavious WHERE wbookname='"+rv_bookname+"'")
    cursor.connection.commit()
    result=mysql.getone("SELECT *FROM wfavious WHERE wbookname='"+rv_bookname+"'")
    if result==None:
        remove_im["status"]=0
        remove_im["desc"]="该书已从你的收藏夹删除!"
        remove_im["uid"]=1
    else:
        remove_im["desc"]="操作取消"
    return json.dumps(remove_im,cls=CJsonEncoder)

@app.route("/card/talk",methods=["POST"])
def add_talk():
    add_result={"status":1,"desc":"发布失败,请检查书名和评分项","uid":0}
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    invitation_bookname=request.json.get("bookname")
    invitation_username=request.json.get("name")
    invitation_star=request.json.get("star")
    invitation_comtent=request.json.get("content")
    invitation_star=str(invitation_star)
    invitation_time=datetime.now()
    book_result=mysql.getone("SELECT *FROM book WHERE wbookname LIKE '%"+invitation_bookname+"%'")
    if book_result!=None:
        book_image=book_result["wbookimage"]
        book_id=book_result["wbookid"]
        book_name=book_result["wbookname"]
        cursor.execute('INSERT INTO invitation (winvitate,winvitatedate,winvitatebookname,winvitatestar,wusername,wbookimage,wbookid) VALUES ("'+invitation_comtent+'","'+invitation_time.strftime('%Y-%m-%d %H:%M:%S')+'","'+book_name+'","'+invitation_star+'","'+invitation_username+'","'+book_image+'","'+str(book_id)+'");')
        cursor.connection.commit()
        talk_result=mysql.getone("SELECT *FROM invitation WHERE winvitatedate='"+invitation_time.strftime('%Y-%m-%d %H:%M:%S')+"' AND wusername='"+invitation_username+"'")
        add_result["info"]=talk_result
        add_result["status"]=0
        add_result["desc"]="提交成功"
        add_result["uid"]=1
    
    else:
        add_result["desc"]="没有找到该书籍,请重试"
    
    return json.dumps(add_result,cls=CJsonEncoder)

@app.route("/card/deletetalk",methods=["POST"])
def delete_talk():
    delete_result={"status":1,"desc":"删除失败","uid":0}
    invitation_bookname=request.json.get("bookname")
    book_result=mysql.getone("SELECT *FROM invitation WHERE winvitatebookname='"+invitation_bookname+"'")
    if book_result!=None:
        mysql.Excuit("DELETE FROM invitation WHERE winvitatebookname='"+invitation_bookname+"'")
        invitate_result=mysql.getone("SELECT *FROM invitation WHERE winvitatebookname='"+invitation_bookname+"'")
        if invitate_result==None:
            delete_result["status"]=0
            delete_result["desc"]="删除成功"
            delete_result["uid"]=1
    return json.dumps(delete_result,cls=CJsonEncoder)
@app.route("/my/message",methods=["POST"])
def send_message():
    message_result={"status":1,"desc":"反馈失败","uid":0}
    message_title=request.json.get("message_title")
    message_content=request.json.get("message_content")
    message_time=datetime.now()
    message_id=request.json.get("message_id")
    message_id=str(message_id)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("INSERT INTO wmessage (wumessagetitle,wumessagecontent,winserttime,wuserid) VALUES ('"+message_title+"','"+message_content+"','"+message_time.strftime('%Y-%m-%d %H:%M:%S')+"','"+message_id+"')")
    cursor.connection.commit()
    message_result["status"]=0
    message_result["desc"]="反馈成功,请等待管理员处理"
    message_result["uid"]=1


    return json.dumps(message_result,cls=CJsonEncoder)

@app.route("/book/read",methods=["POST"])
def get_txt():
    book_result={"status":1,"desc":"读取失败","uid":0}
    book_id=request.json.get("bookid")
    book=mysql.getone("SELECT *FROM book WHERE wbookid="+str(book_id))
    book_url=book["wbooktxt"]
    if book!=None:
        with open(book_url,'r',encoding='utf-8') as f:
            book_result["bookdata"]=f.read()
            book_result["status"]=0
            book_result["desc"]="读取成功"
            book_result["uid"]="1"
            book_result["book"]=book
    
    return json.dumps(book_result,cls=CJsonEncoder)

@app.route("/admin/seeuser")
def see_user():
    user_result={"status":1,"desc":"系统中没有用户注册","uid":0}
    result=mysql.doIt("SELECT wuserid,wusername,wuserphone,wuserinsert_time,walimit FROM wuser")
    if len(result)!=0:
        user_result["status"]=0
        user_result["desc"]=f"系统中有{len(result)}名用户"
        user_result["uid"]=1
        user_result["data"]=result
    
    return json.dumps(user_result,cls=CJsonEncoder)

@app.route("/admin/seemessage")
def see_message():
    message_result={"status":1,"desc":"没有反馈消息","uid":0}
    result=mysql.doIt("SELECT *FROM wmessage ORDER BY wumessageid DESC;")
    if len(result)!=0:
        message_result["status"]=0
        message_result["desc"]=f"系统中有{len(result)}条反馈消息"
        message_result["uid"]=1    
        message_result["data"]=result
    
    return json.dumps(message_result,cls=CJsonEncoder)

@app.route("/my/wodeshoucang",methods=["POST"])
def get_my_favious():
    favious_result={"status":1,"desc":"没有发布帖子"}
    username=request.json.get("username")
    result=mysql.doIt("SELECT *FROM invitation where wusername='"+username+"'")
    if len(result)!=0:
        favious_result["status"]=0
        favious_result["desc"]="查询成功"
        favious_result["data"]=result
    
    return json.dumps(favious_result,cls=CJsonEncoder)

@app.route("/my/remove_favious",methods=["POST"])
def remove_favious():
    message_result={"status":1,"desc":"删除失败"}
    iid=request.json.get("iid")
    uname=request.json.get("username")
    result=mysql.getone("SELECT *FROM invitation WHERE wusername='"+uname+"' AND winvitateid='"+str(iid)+"'")
    if result!=None:
        mysql.Excuit("DELETE FROM invitation WHERE wusername='"+uname+"' AND winvitateid='"+str(iid)+"'")
        message_result["status"]=0
        message_result["desc"]="删除成功"


    return json.dumps(message_result,cls=CJsonEncoder)

@app.route("/my/wodefankui",methods=["POST"])
def get_my_message():
    message_result={"status":1,"desc":"没有反馈消息"}
    userid=request.json.get("userid")
    result=mysql.doIt("SELECT *FROM wmessage where wuserid="+str(userid))
    if len(result)!=0:
        message_result["status"]=0
        message_result["desc"]="查询成功"
        message_result["data"]=result

    return json.dumps(message_result,cls=CJsonEncoder)

@app.route("/my/remove_message",methods=["POST"])
def remove_message():
    message_result={"status":1,"desc":"删除失败"}
    mid=request.json.get("mid")
    uid=request.json.get("userid")
    result=mysql.getone("SELECT *FROM wmessage WHERE wuserid='"+str(uid)+"' AND wumessageid='"+str(mid)+"'")
    if result!=None:
        mysql.Excuit("DELETE FROM wmessage WHERE wuserid='"+str(uid)+"' AND wumessageid='"+str(mid)+"'")
        message_result["status"]=0
        message_result["desc"]="删除成功"


    return json.dumps(message_result,cls=CJsonEncoder)

@app.route("/admin/place",methods=["POST"])
def manage_place():
    place_result={"status":1,"desc":"没有该帖子","uid":0}
    invitate_id=request.json.get("invitateid")
    result=mysql.getone("SELECT *from invitation WHERE invitateid="+str(invitate_id))
    if result!=None:
        mysql.Excuit("DELETE FROM invitation WHERE invitateid="+str(invitate_id))
        return_result=mysql.getone("SELECT *from invitation WHERE invitateid="+str(invitate_id))
        if return_result==None:
            place_result["status"]=0
            place_result["desc"]="帖子已删除!"
            place_result["uid"]=1
        else:
            place_result["desc"]="删除失败,请稍微再试"
    

    return json.dumps(place_result,cls=CJsonEncoder)

@app.route("/admin/seeplace")
def see_place():
    see_place_result={"status":1,"desc":"暂时无人发布帖子","uid":0}
    result=mysql.doIt("SELECT *FROM invitation")
    if len(result)!=0:
        see_place_result["status"]=0
        see_place_result["desc"]=f"系统中有{len(result)}个帖子"
        see_place_result["uid"]=1
        see_place_result["data"]=result

    return json.dumps(see_place_result,cls=CJsonEncoder)

@app.route("/admin/book",methods=["POST"])
def manage_book():
    delete_result={"status":1,"desc":"没有该书籍","uid":0}
    book_id=request.json.get("bookid")
    result=mysql.getone("SELECT *from book WHERE wbookid="+str(book_id))
    if result!=None:
        mysql.Excuit("DELETE FROM book WHERE wbookid="+str(book_id))
        return_result=mysql.getone("SELECT *from book WHERE wbookid="+str(book_id))
        if return_result==None:
            delete_result["status"]=0
            delete_result["desc"]="书籍已删除!"
            delete_result["uid"]=1
        else:
            delete_result["desc"]="删除失败,请稍微再试"
    

    return json.dumps(delete_result,cls=CJsonEncoder)

@app.route("/card/imformation",methods=["POST"])
def add_imformation():
    im_result={"status":1,"desc":"请勿发布相同的公告","uid":0}
    title=request.json.get("title")
    name=request.json.get("name")
    content=request.json.get("content")
    inserttime=datetime.now()
    walimit=str(999)
    result=mysql.getone("SELECT *FROM waim WHERE waimtitle='"+title+"' AND waimcontent='"+content+"' AND wadminname='"+name+"'")
    if result==None:
        mysql.Excuit('INSERT INTO waim (waimtitle,waimcontent,waimdate,wadminname,walimit) VALUES("'+title+'","'+content+'","'+inserttime.strftime('%Y-%m-%d %H:%M:%S')+'","'+name+'","'+walimit+'")')
        result_one=mysql.getone("SELECT *FROM waim WHERE waimtitle='"+title+"' AND waimcontent='"+content+"' AND wadminname='"+name+"'")
        if result_one!=None:
            im_result["status"]=0
            im_result["desc"]="发布成功"
            im_result["uid"]=1
        else:
            im_result["desc"]="发布失败"
    return json.dumps(im_result,cls=CJsonEncoder)

@app.route("/card/adminim")
def get_adminim():
    adminim_result={"status":1,"desc":"获取失败,暂无公告"}
    result=mysql.doIt("SELECT *FROM waim")
    if len(result)!=0:
        adminim_result["status"]=0
        adminim_result["desc"]="获取成功"
        adminim_result["data"]=result
    
    return json.dumps(adminim_result,cls=CJsonEncoder)

@app.route("/admin/deleteim",methods=["POST"])
def delete_im():
    adminim_result={"status":1,"desc":"删除失败,暂无公告"}
    waimid=request.json.get("waimid")
    mysql.Excuit("DELETE FROM waim WHERE waimid="+str(waimid))
    result=mysql.getone("SELECT *FROM waim WHERE waimid="+str(waimid))
    if result==None:
        adminim_result["status"]=0
        adminim_result["desc"]="公告删除成功!"

    return json.dumps(adminim_result,cls=CJsonEncoder)

# @app.route("/admin/updatebook",methods=["POST"])
# def update_book():
#     adminim_result={"status":1,"desc":"删除失败"}
#     bookname=request.json.get("bookname")
#     bookimage=request.json.get("bookimage")
#     bookpdesc=request.

@app.route("/index/displaylist",methods=["POST"])
def displaylist():
    user_id=request.json.get("userid")
    display_result={"status":1,"desc":"查询失败,暂无推荐"}
    result=mysql.doIt("SELECT *FROM wtcontent WHERE wuserid="+str(user_id))
    if len(result)!=0:
        display_result["status"]=0
        display_result["desc"]="显示成功"
        display_result["data"]=result
    
    return json.dumps(display_result,cls=CJsonEncoder)


@app.route("/index/tuijian",methods=["POST"])
def tuijian():
    all_result={"status":1,"desc":"查询失败,请联系管理员"}
    result=[]
    catetory=[]
    catetory_count={}
    book_all=[]
    catetory_name=[]
    num=0
    userid=request.json.get("userid")
    new_insert_time=datetime.now()
    now_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # wadmin_result=mysql.getone("SELECT *FROM adminuser WHERE waid="+str(userid))
    wuser_result=mysql.getone("SELECT *FROM wuser WHERE wuserid="+str(userid))
    if wuser_result!=None:
        wuser_id=wuser_result["wuserid"]
        wuser_name=wuser_result["wusername"]
        wuser_tcontent=mysql.doIt("SELECT *FROM wtcontent WHERE wuserid="+str(wuser_id))
        wuser_fresult=mysql.doIt("SELECT *FROM wfavious WHERE wusername='"+wuser_name+"'")
        if len(wuser_tcontent)==0:
            book_len=mysql.doIt("SELECT *FROM book")
            book_len=len(book_len)
            wtcontent_rand=[random.randint(0,book_len) for _ in range(10)]
            for content in wtcontent_rand:
                 mysql_c=mysql.doIt("SELECT *FROM book WHERE wbookid="+str(content)) # 向推荐表中添加数据
                 result.extend(mysql_c)
                #  print(mysql_c)
                #  print('\n')
                 mysql.Excuit('INSERT INTO wtcontent (wbookid,wtbookname,wyid,wtbookimage,wuserid,wtinsertdate) VALUES ("'+str(content)+'","'+mysql_c[0]["wbookname"]+'","'+str(mysql_c[0]["wyid"])+'","'+mysql_c[0]["wbookimage"]+'","'+str(wuser_id)+'","'+new_insert_time.strftime('%Y-%m-%d %H:%M:%S')+'")')
             #此人为新用户,执行随机推荐十本书

            all_result["tbook"]=result
            all_result["status"]=0
            all_result["desc"]="推荐成功"

        elif len(wuser_tcontent)!=0: # 当不是新用户时
            tbook_time=mysql.getone("SELECT *FROM wtcontent WHERE wuserid="+str(wuser_id))
            tbook_time_1=tbook_time["wtinsertdate"].strftime('%Y-%m-%d %H:%M:%S')
            hours=now_time[8:10]
            hours=str(hours)
            ess_time=now_time[0:8]+hours+' 00:00:00'
            if tbook_time_1>ess_time: # 当推荐表时间大于今日00.00.00时
                already_book=mysql.doIt("SELECT *FROM wtcontent WHERE wuserid="+str(wuser_id))
                all_result["status"]=0
                all_result["desc"]="今日已推荐"
                all_result["tbook"]=already_book
                
            elif tbook_time_1<ess_time: # 当推荐表时间小于今日00；00；00时
                wuser_id=wuser_result["wuserid"]
                wuser_name=wuser_result["wusername"]
                wuser_fresult=mysql.doIt("SELECT *FROM wfavious WHERE wusername='"+wuser_name+"'")
                if len(wuser_fresult)==0:
                    mysql.Excuit("DELETE FROM wtcontent WHERE wuserid in ('"+str(wuser_id)+"')")
                    book_len=mysql.doIt("SELECT *FROM book")
                    book_len=len(book_len)
                    wtcontent_rand_1=[random.randint(0,book_len) for _ in range(10)]
                    for content in wtcontent_rand_1:
                        mysql_c=mysql.doIt("SELECT *FROM book WHERE wbookid="+str(content)) # 向推荐表中添加数据
                        result.extend(mysql_c)
                        mysql.Excuit('INSERT INTO wtcontent (wbookid,wtbookname,wyid,wtbookimage,wuserid,wtinsertdate) VALUES ("'+str(content)+'","'+mysql_c[0]["wbookname"]+'","'+str(mysql_c[0]["wyid"])+'","'+mysql_c[0]["wbookimage"]+'","'+str(wuser_id)+'","'+new_insert_time.strftime('%Y-%m-%d %H:%M:%S')+'")')
                    all_result["tbook"]=result
                    all_result["status"]=0
                    all_result["desc"]="推荐成功"
                else:
                    user_name=mysql.getone("SELECT *FROM wuser WHERE wuserid="+str(wuser_id))
                    mysql.Excuit("DELETE FROM wtcontent WHERE wuserid in ('"+str(wuser_id)+"')")
                    yet_book=mysql.doIt("SELECT *FROM wfavious WHERE wusername='"+user_name['wusername']+"'")
                    for yet_book_single in yet_book:
                        book_all.append(yet_book_single["wbookname"]) # 取出收藏夹中书籍的名字

                    for i in book_all:
                        book_single=mysql.getone("SELECT wyid,wbookname,wbookid from book WHERE wbookname='"+i+"'")
                        catetory.append(book_single["wyid"])

                    for i in catetory:
                        catetory_single=mysql.getone("SELECT *from wcategory WHERE wyid="+str(i))
                        catetory_name.append(catetory_single["wyid"])
                                               
                    for yid in catetory_name:
                        count=catetory.count(yid)
                        catetory_count[yid]=count #收藏夹中某一类文学出现的次数
                    
                    for value in catetory_count.values():
                        num=num+value

                    for key in catetory_count.keys():
                        key_float=catetory_count[key]/num
                        key_book_de=key_float*10
                        key_book_de=int(key_book_de)
                        key_book=mysql.doIt("SELECT *from book WHERE wyid="+str(key))
                        len_key=len(key_book)
                        wtconbook=[random.randint(0,len_key) for _ in range(key_book_de)]
                        for j in wtconbook:
                            tbook=key_book[j]
                            mysql.Excuit("INSERT INTO wtcontent (wbookid,wtbookname,wyid,wtbookimage,wuserid,wtinsertdate) VALUES ('"+str(tbook['wbookid'])+"','"+tbook['wbookname']+"','"+str(key)+"','"+tbook['wbookimage']+"','"+str(wuser_id)+"','"+new_insert_time.strftime('%Y-%m-%d %H:%M:%S')+"')")
                        
                    all_result["status"]=0
                    all_result["desc"]="推荐成功"

    return json.dumps(all_result,cls=CJsonEncoder)

@app.route("/index/randbook")
def getrandbook():
    one=str(random.randint(743,842))
    two=str(random.randint(643,742))
    three=str(random.randint(343,542))
    four=str(random.randint(143,342))
    five=str(random.randint(0,142))
    six=str(random.randint(543,642))
    banner_1=mysql.getone("SELECT *FROM book WHERE wbookid='"+one+"';")
    banner_2=mysql.getone("SELECT *FROM book WHERE wbookid='"+two+"';")
    banner_3=mysql.getone("SELECT *FROM book WHERE wbookid='"+three+"';")
    banner_4=mysql.getone("SELECT *FROM book WHERE wbookid='"+four+"';")
    banner_5=mysql.getone("SELECT *FROM book WHERE wbookid='"+five+"';")
    banner_6=mysql.getone("SELECT *FROM book WHERE wbookid='"+six+"';")
    banner={"banner_1":banner_1,"banner_2":banner_2,"banner_3":banner_3,"banner_4":banner_4,"banner_5":banner_5,"banner_6":banner_6}
    return json.dumps(banner,cls=CJsonEncoder)

@app.route("/test/test")
def gettest():
    id=request.args.get("uid")
    rs=redis.StrictRedis(config.redisConfig["host"],config.redisConfig["port"])
    #rs.hset("cart")
    msg=rs.hget("cart","u"+str(id))
    if msg==None:
        rs.hset("cart","u"+str(id),"[]")
    msg=rs.hget("cart","u"+str(id))
    return json.dumps(json.loads(msg))

@app.route("/my/changeun",methods=["POST"])
def changeimname():
    name=request.json.get("name")
    id=request.json.get("userid")
    old_name=request.json.get("old_name")
    imn_result_1={"status":1,"desc":"系统繁忙"}
    imn_result=mysql.doIt("SELECT *from wuser where wusername='"+name+"'")
    if len(imn_result)==0:
        mysql.Excuit("UPDATE wuser SET wusername='"+name+"' where wuserid='"+str(id)+"'")
        mysql.Excuit("UPDATE invitation SET wusername='"+name+"'where wusername='"+old_name+"' ")
        mysql.Excuit("UPDATE wfavious SET wusername='"+name+"'where wusername='"+old_name+"' ")
        imn_result_1["status"]=0
        imn_result_1["desc"]="修改成功"
    else:
        imn_result_1["desc"]="用户名已存在"
    
    return json.dumps(imn_result_1,cls=CJsonEncoder)

@app.route("/my/changipas",methods=["POST"])
def changepas():
    phone=request.json.get("phone")
    userid=request.json.get("userid")
    old_password=request.json.get("old_password")
    new_password=request.json.get("new_password")
    code=request.json.get("code")
    pas_result={"status":1,"desc":"系统繁忙"}
    old_password=hashlib.sha1(old_password.encode()).hexdigest()
    new_password=hashlib.sha1(new_password.encode()).hexdigest()
    # pas=mysql.doIt("select *from wuser where wuserid="+str(userid))
    im_pas=mysql.doIt("select *from wuser where wuserid='"+str(userid)+"' and wuserpassword='"+old_password+"'")
    res_code=mysql.doIt("select *from user_code where phone='"+str(phone)+"' and code='"+str(code)+"'")
    if len(res_code)==0:
        pas_result["desc"]="验证码输入错误"
    else:
        mysql.Excuit("UPDATE wuser SET wuserpassword='"+new_password+"' where wuserid='"+str(userid)+"'")
        nw_pas=mysql.doIt("select *from wuser where wuserid='"+str(userid)+"' and wuserpassword='"+new_password+"'")
        if len(nw_pas)==0:
            pas_result["desc"]="修改失败,请稍后再试"
        else:
            pas_result["status"]=0
            pas_result["desc"]="修改成功"
    
    return json.dumps(pas_result,cls=CJsonEncoder)

@app.route("/my/userimfor",methods=["POST"])
def getim():
    userid=request.json.get("id")
    pas_result={"status":1,"desc":"系统繁忙"}
    result=mysql.doIt("select *from wuser where wuserid="+str(userid))
    if len(result)!=0:
        pas_result["status"]=0
        pas_result["desc"]="修改成功"
        pas_result["data"]=result[0]

    return json.dumps(pas_result,cls=CJsonEncoder)





app.run(host="172.20.10.6",port=4444,debug=True)
