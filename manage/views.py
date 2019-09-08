# _*_ coding: utf-8 _*_
import json
from django.core import serializers
import random
from collections import Counter
from django.shortcuts import redirect
import datetime
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manage.models import *
import smtplib
from email.mime.text import MIMEText
import string
import random
import time
import datetime
class message(View):
    def changeReadStatus(request):
        id = json.loads(request.body)['id']
        try:
            Message.objects.filter(id=id).update(is_read=1)
            return JsonResponse({'msg':'success'},status = 200)
        except:
            return JsonResponse({'msg':'fail'},status = 400)
    def agreeMessage(request):
        data = json.loads(request.body)
        receive_suggestion = data['suggestion']
        title = data['title']
        id = data['id']
        objj = Message.objects.filter(id = id)
        if title == 'agree':
            objj.update(is_read =1 ,is_pass=1,end_time = datetime.datetime.now(),receive_suggestion =receive_suggestion)
            seat_id = objj.values('seat_id')[0]['seat_id']
            if  seat_id != None:
                status  =  Seat.objects.filter(seat_id = seat_id).values('status')[0]['status']
                if status  ==  2:
                    Seat.objects.filter(seat_id=seat_id).update(status = 0,department_id = 14)
                elif status == 4:
                    Seat.objects.filter(seat_id=seat_id).update(status = 3,department_id = 14)
                elif status == 7:

                    Seat.objects.filter(seat_id=seat_id).update(status = 6,department_id = 14)
            return JsonResponse({'msg':'successful','obj':1},status = 200)
        elif title == 'disagree':
            Message.objects.filter(id = id).update(is_read =1 ,is_pass=2,end_time = datetime.datetime.now(),receive_suggestion =receive_suggestion)
            return JsonResponse({'msg':'successful','obj':0},status = 200)

    def messageDetail(request):
        data = json.loads(request.body)
        id = data['id']
        try:
            user_id  =   Message.objects.filter(id = id).values('send_user_id')[0]['send_user_id']

            d = Users.objects.filter(user_id = user_id).values('department__name','name')[0]
            department = d['department__name']
            name = d['name']
            obj = list(Message.objects.filter(id = id).values('deleted','title','count','type','send_time','end_time','read_time','id','send_user_id','seat_id','send_status','receive_suggestion','send_msg','is_read','is_pass'))[0]

            obj['department'] = department
            obj['name'] = name
            return JsonResponse({'msg':obj},status =  200)
        except:
            return JsonResponse({'msg':'Fail'},status =  400)

    def delMsg(request):
        data = json.loads(request.body)
        id = data['id']
        try:
            Message.objects.filter(id = id).update(deleted = 1)
            return JsonResponse({'msg':'Ok'},status =  200)
        except:
            return JsonResponse({'msg':'Fail'},status =  400)

    def msgWindow(request):
        return JsonResponse({'count':10},status = 200)

    def messageDetailForm(request):
        role = request.session[request.COOKIES['user']]['role_id']
        return render(request,'message/messageDetail.html',{'role':role},status = 200)

    def sendEmail(send_name,receive_user_email,msg):
        try:
            mailserver = "mail.iflytek.com"  # 邮箱服务器地址
            send_email= 'welcome@iflytek.com'  # 邮箱用户名
            password = 'rect!2016'  # 邮箱密码：需要使用授权码
            username_recv = receive_user_email  # 收件人，多个收件人用逗号隔开
            mail = MIMEText("%s" %(msg))
            mail['Subject'] = '来自%s的工位系统申请' % (send_name)
            mail['From'] = send_name  # 发件人
            mail['To'] = receive_user_email  # 收件人；
            smtp = smtplib.SMTP(mailserver, port=25)  # 连接邮箱服务器，smtp的端口号是25
            # smtp=smtplib.SMTP_SSL('smtp.qq.com',port=465) #QQ邮箱的服务器和端口号
            smtp.login(send_email, password)  # 登录邮箱
            smtp.sendmail(send_email, username_recv, mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
            smtp.quit()  # 发送完毕后退出smtp
            return JsonResponse({'msg':0},status = 200)
        except:
            return JsonResponse({'msg': 1}, status=400)

    def sendMessageToAdmin(request):
        data = json.loads(request.body)
        send_user_id = data['user_id']
        seat_id = data['seat_id']
        send_msg = data['send_msg']
        send_email = 'welcome@iflytek.com'
        receive_user_email = 'dfxie@iflytek.com'
        msg = message.sendEmail(send_email,send_user_id,receive_user_email,send_msg,seat_id)
        send_time =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if msg == 'success':
            Message.objects.create(send_user_id = send_user_id , receive_user_id = '000001' , receive_user_email = receive_user_email , seat_id = seat_id , send_status = 1 ,send_msg = send_msg ,is_read = 0 ,is_pass = 0 ,send_time =send_time)
            return JsonResponse({'msg':'ok'},status =200)

                       #写审批意见
    def writeSuggestion(request):
        try:
            data = json.loads(request.body)
            id = data['id']
            receive_suggestion = data['receive_suggestion']
            Message.objects.filter(id = id).update(receive_suggestion = receive_suggestion)
            return JsonResponse({'msg':'ok'},status = 200)
        except:
            return JsonResponse({'msg':'fail'},status = 400)
        #改变sendmsg
    def changeSendMsg(request):
        try:
            data = json.loads(request.body)
            id = data['id']
            send_msg = data['send_msg']
            Message.objects.filter(id = id).update(send_msg = send_msg)
            return JsonResponse({'msg':'ok'},status = 200)
        except:
            return JsonResponse({'msg':'fail'},status =400)


    def messageList(request):

        try:
            dic = {}
            obj = []

            cookie_content = request.COOKIES
            user = cookie_content['user']
            userInfo = request.session[user]
            user_id = userInfo['user_id']
            name = userInfo['name']
            role = userInfo['role_id']
            if role == 0 :
                obj = list(Message.objects.filter(deleted = 0).order_by('-id'))
            else:
                obj = list(Message.objects.filter(send_user_id = user_id,deleted = 0).order_by('-id'))
            return render(request, 'message/message-list.html', {'message':obj, 'role':role, 'count':len(obj)},status = 200)
        except:
            return render(request, 'message/message-list.html', status = 400)


class index(View):

    def contextMenuTest(request):
        return render(request,'contextMuneTest.html')










    def echarts1(request):
        return render(request, 'echarts1.html')
    def echarts2(request):
        return render(request, 'echarts2.html')
    def echarts3(request):
        return render(request, 'echarts3.html')
    def echarts4(request):
        return render(request, 'echarts4.html')
    def echarts5(request):
        return render(request, 'echarts5.html')
    def echarts6(request):
        return render(request, 'echarts6.html')
    def echarts7(request):
        return render(request, 'echarts7.html')
    def echarts8(request):
        return render(request, 'echarts8.html')














    def unicode(request):
        return render(request,'unicode.html')

class Seats(View):
    def delSeat(request):
        Seat.objects.delete()

class Members(View):
    def adminlist(request):
        res = Users.objects.filter(Q(role = 0) | Q(role = 1) | Q(role = 2)  , deleted = 0)
        return render(request,'admin-list.html', {'user': res})


    def adminrule(request):
        return render(request,'admin-rule.html')
    def admincate(request):
        return render(request,'admin-cate.html')

    def memberpassword(request):
        return render(request,'member-password.html')




class Admin(View):


    def delGroup(request):
        data = json.loads(request.body)
        try:
            id = data['id']
            Group.objects.filter(id = id).delete()
            return JsonResponse({'msg':'刪除成功'},status = 200)
        except:
            return JsonResponse({'msg': '刪除失敗'}, status=400)

    #status为1的在执行操作时需要重新获得session
    # 0 需要重新获取 1不需要
    def changeSession(title,id):
        try:
            if title == 'group':
                Users.objects.filter(group_id = id).update(status = 0)
            elif title == 'user':
                Users.objects.filter(user_id = id).update(status = 0)
            elif title == 'id':
                Users.objects.filter(id = id).update(status = 0)
            return 'ok'
        except:
            return 'fail'

    def setGroup(request):
        if request.method == 'GET':
            obj = list(Group.objects.filter(~Q(id = 3)).values('id','name'))
            return render(request,'admin/setGroup.html',{'obj':obj},status = 200)
        if request.method == 'POST':
            data = json.loads(request.body)
            user = request.COOKIES['user']
            userInfo = request.session[user]
            status = Users.objects.filter(user_id=userInfo['user_id']).values('status')[0]['status']
            user_id = userInfo['user_id']
            if status == 0:
                userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
            if '3' not in userInfo['func_list']:
                return JsonResponse({'msg':'无权限'},status = 400)
            group_id  =  data['group_id']
            id = data['id']
            Users.objects.filter(id = id).update(group_id = group_id)
            Admin.changeSession('id',id)
            return JsonResponse({'msg':'设置成功'},status = 200)


    def ChangeCookiesAndSession(request,user,user_id):
        User = list(Users.objects.filter(user_id = user_id).values('user_id','name','role_id','department_id','group_id__name','group_id__depart_list','group_id__func_list'))[0]
        depart_list = User['group_id__depart_list'].split(',')
        func_list = User['group_id__func_list'].split(',')
        userInfo = {'user_id': User['user_id'], 'name': User['name'], 'role_id': User['role_id'], 'department_id': User['department_id'],'group_name': User['group_id__name'],'depart_list': depart_list, 'func_list': func_list}
        request.session[user] = userInfo
        request.session.set_expiry(1 * 60 * 60 * 24)
        Users.objects.filter(user_id=user_id).update(status = 1)
        return userInfo




    def changeGroup(request):
        data = json.loads(request.body)
        try:
            id = data['id']
            title = data['title']
            value = data['value']
            if title == '分组描述':
                Group.objects.filter(id = id).update(describe = value)
            else:
                Group.objects.filter(id=id).update(name = value)
            return JsonResponse({'msg':'修改成功'},status = 200)
        except:
            return JsonResponse({'msg':'修改失败'},status = 400)




    #改变分组可管理部门
    def changeGroupDepart(request):
        data = request.POST
        try:
            group_id = data.get('group_id')
            id = data.get('id')
            DepartChanged = data.get('DepartChanged')
            depart_list = Group.objects.filter(id=group_id).values('depart_list')[0]['depart_list'].split(',')
            # 找到值 ， false就从str中去除，true就加到str中
            if DepartChanged == 'false':
                # 列表中去除，转化成str存进去
                depart_list.remove(id)
                depart_list = ",".join(depart_list)
                if depart_list == '':
                    depart_list = 0
                Group.objects.filter(id=group_id).update(depart_list=depart_list)
                changeStatus = Admin.changeSession('group',group_id)
                if changeStatus == 'ok':
                    return JsonResponse({'msg': '去除成功'}, status=200)
            elif DepartChanged == 'true':
                # 列表中增加，转化成str存进去
                if '0' in depart_list:
                    depart_list.remove('0')
                depart_list.append(id)
                depart_list = ",".join(depart_list)
                if depart_list[0] == ',':
                    depart_list = depart_list[1:]
                Group.objects.filter(id=group_id).update(depart_list=depart_list)
                changeStatus = Admin.changeSession('group', group_id)
                if changeStatus == 'ok':
                    return JsonResponse({'msg': '增加成功'}, status=200)
                # return JsonResponse({'msg': '增加成功'}, status=200)
        except:
            return JsonResponse({'msg': '更改失败'}, status=400)

    #改变分组功能权限
    def changeGroupFunc(request):
        data = request.POST
        try:
            group_id = data.get('group_id')
            id = data.get('id')
            FuncChanged = data.get('FuncChanged')
            func_list = Group.objects.filter(id = group_id).values('func_list')[0]['func_list'].split(',')
            # 找到值 ， false就从str中去除，true就加到str中
            if FuncChanged == 'false':
                # 列表中去除，转化成str存进去
                func_list.remove(id)
                func_list = ",".join(func_list)
                if func_list == '':
                    func_list = 0
                    # Group.objects.filter(id=group_id).update(func_list=func_list)
                Group.objects.filter(id = group_id).update(func_list = func_list)
                changeStatus = Admin.changeSession('group',group_id)
                if changeStatus == 'ok':
                    return JsonResponse({'msg': '去除成功'}, status=200)
                return JsonResponse({'msg': '去除成功'}, status=200)
            elif FuncChanged == 'true':
                # 列表中增加，转化成str存进去
                func_list.append(id)
                if '0' in func_list:
                    func_list.remove('0')
                func_list = ",".join(func_list)
                if func_list[0] == ',':
                    func_list = func_list[1:]
                Group.objects.filter(id=group_id).update(func_list=func_list)
                changeStatus = Admin.changeSession('group',group_id)
                if changeStatus == 'ok':
                    return JsonResponse({'msg': '增加成功'}, status=200)
        except:
            return JsonResponse({'msg': '更改失败'}, status=400)






    def adminEdit(request):
        return render(request,'admin-edit.html',status = 200)
    def editRole(request,id):
        if request.method == 'GET':
            # 传页面部门信息id，和功能信息id
            # 传页面部门信息
            groupList = list(Group.objects.filter(id = id).values('id','name','depart_list','func_list'))[0]
            Department_list = list(Department.objects.filter(deleted = 0).values('id', 'name'))
            depart_list  = groupList['depart_list'].split(',')
            func_list = groupList['func_list'].split(',')
            Func_list = list(Func.objects.filter().values('id','name'))
            obj = []
            func = []
            for i in Department_list:
                if (str(i['id']) in depart_list):
                    oneDict = {'id':i['id'],'name':i['name'],'status':1}
                else:
                    oneDict = {'id': i['id'], 'name': i['name'], 'status': 0}
                obj.append(oneDict)
            for u in Func_list:
                if str(u['id']) in func_list:
                    oneDict = {'id': u['id'], 'name': u['name'], 'status': 1}
                else:
                    oneDict = {'id': u['id'], 'name': u['name'], 'status': 0}
                func.append(oneDict)
            return render(request,'admin/editRole.html',{'depart_list':obj,'func_list':func,'id':id},status = 200)

    def groupAdd(request):
        if request.method == 'GET':
            return render(request,'admin/group-add.html',status = 200)

        if request.method == 'POST':
            data = json.loads(request.body)
            try:
                nameList = list(Group.objects.filter().values('name'))
                name = data['name']
                for ii in nameList:
                    if name == ii['name']:
                        return JsonResponse({'msg': '分组已存在'}, status=400)
                describe = data['describe']
                Group.objects.create(name = name , describe = describe,depart_list=0,func_list=0)
                id = Group.objects.filter(name = name ).values('id')[0]['id']
                return JsonResponse({'msg':'创建成功','id':id,'name':name,'describe':describe},status = 200)
            except:
                return JsonResponse({'msg':'创建失败，请重试'},status = 400)


    def adminrole(request):
        info = list(Users.objects.filter(~Q(group_id=3)).values('group_id','name','group_id__name','group_id__describe').order_by('group_id'))
        noDe = list(Group.objects.filter(~Q(id = 3)).values())
        allDict = {}
        obj = []
        for i in noDe:
            allDict[i['id']] = {'id': i['id'], 'name': i['name'], 'describe': i['describe'], 'user': ''}
        for u in info:
            id = u['group_id']
            name = u['name']
            if allDict[id]['user'] == '':
                allDict[id]['user'] += '%s' % (name)
            else:
                allDict[id]['user'] += ',%s' %(name)
        for one in allDict:
            obj.append(allDict[one])
        return render(request, 'admin/role.html',{'obj':obj})

class UserClass(View):
# 编辑用户
    def editUser(request):
        if request.method == 'GET':
            return render(request,'user/edit.html',status = 200)
        if request.method == 'POST':
            data = json.loads(request.body)
            try:
                user = request.COOKIES['user']
                userInfo = request.session[user]
                status = Users.objects.filter(user_id=userInfo['user_id']).values('status')[0]['status']
                user_id = userInfo['user_id']
                if status == 0:
                    userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
                if '16' not in userInfo['func_list']:
                    return JsonResponse({'msg':'无编辑用户权限'},status = 400)

                id = data['id']
                name = data['name']
                Users.objects.filter(id = id).update(name = name)
                return JsonResponse({'msg': '编辑成功'}, status=200)
            except:
                return JsonResponse({'msg':'错误'},status = 400)

        # if request.method == 'POST':

#用戶新增

    def memberadd(request):
        if request.method == 'GET':
            return render(request,'user/member-add.html')
        if request.method == 'POST':
            user = request.COOKIES['user']
            userInfo = request.session[user]
            status = Users.objects.filter(user_id=userInfo['user_id']).values('status')[0]['status']
            user_id = userInfo['user_id']
            if status == 0:
                userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
            if '15' not in userInfo['func_list']:
                return  JsonResponse({'msg':'无新增用户权限'},status = 400)
            data = json.loads(request.body)
            name = data['name']
            department_id = data['department_id']
            user_id = data['user_id']
            obj = Users.objects.filter(user_id = user_id,deleted = 0)
            if obj.exists():
                return JsonResponse({'msg': '工号已存在'}, status=400)
            if Users.objects.filter(user_id=user_id, deleted=1).exists():
                Users.objects.filter(user_id=user_id).update(role = 3,user_id=user_id, name=name,
                                                             join_time=datetime.datetime.now(),
                                                             department_id=department_id, status=1, deleted=0,
                                                             group_id=3)
                return JsonResponse({"msg": "成功更新员工"}, status=200)

            else:
                Users.objects.create(name = name,user_id = user_id , department_id = department_id , join_time = datetime.datetime.now(),status = 1,password = '123456',role_id = 3,deleted = 0,group_id = 3)
                return JsonResponse({'msg':'添加成功'},status = 200)
    def depart(request):
        if request.method == 'GET':
            return render(request,'user/department.html',status = 200)
        if request.method == 'POST':
            obj = list(Department.objects.filter(~Q(id=14) & Q(deleted = 0)).values('id', 'name'))
            seat = list(Seat.objects.filter(~Q(department_id=14)).values('department_id'))
            val = {}
            for i in seat:
                id = i['department_id']
                if id in val:
                    val[id] += 1
                else:
                    val[id] = 1
            depart = []
            for u in obj:
                id = u['id']
                if id in val:
                    u['value'] = val[id]
                    u.pop('id')
                    depart.append(u["name"])
                else:
                    u["value"] = 0
                    u.pop('id')
                    depart.append(u["name"])
            # return render(request,'user/department.html',{"obj":obj,'depart':depart},status = 200)
            return JsonResponse({'obj':obj,'depart':depart},status = 200)



    def getUserDepartmentInfo(request):
        data = [{'name': '科大讯飞','itemStyle': {'normal': {'color': '#FF7853'}},'children': []}];
        user = Users.objects.filter(deleted = 0).values('name','department_id__name').order_by('department_id__name')
        list = []
        depart = []
        num = 0
        countUser = len(user)
        oneNum = 0
        for u in user:
            name = u['name']
            departname = u['department_id__name']
            if departname not in list:
                if depart:
                    data[0]['children'].append(depart)
                list.append(departname)
                num += 1
                depart = {'name': departname, 'children': [{'name': '%s☆' % (num), 'children': []}, ]}
                depart['children'][0]['children'].append({'name':name})
                oneNum+=1
            else:
                depart['children'][0]['children'].append({'name':name})
                oneNum+=1
            if oneNum == countUser:
                data[0]['children'].append(depart)
        return JsonResponse({'msg':data},status = 200)




    #登录检查
    def loginCheck(request):
        if request.method == 'GET':
                try:
                    cookie_content = request.COOKIES
                    session_content = request.session
                    user = cookie_content['user']
                    userInfo = request.session[user]
                    domain_accounts = userInfo['domain_accounts']


                    if domain_accounts:
                        status = Users.objects.filter(domain_accounts=userInfo['domain_accounts']).values('status')[0]['status']
                        if status == 0:
                            userInfo = Admin.ChangeCookiesAndSession(request, user, domain_accounts)
                        name = userInfo['name']
                        role = userInfo['role_id']
                        user_id = userInfo['user_id']
                        department_id = userInfo['department_id']
                        group_name = userInfo['group_name']
                        depart_list = userInfo['depart_list']
                        func_list = userInfo['func_list']

                        if role == 0:
                            msgCount = Message.objects.filter(is_read = 0,deleted = 0).count()
                            return  render(request, 'index.html',{'user_id': user_id,'name':name,'role':role,'department_id':department_id,'msgCount':msgCount,'group_name':group_name,'depart_list':depart_list,'func_list':func_list,'show_depart':1,'show_member':1})
                        else:
                            show_depart = 1
                            show_member = 1
                            if ('11' not in func_list) or ('12' not in func_list) or ('13' not in func_list):
                                show_depart = 0
                            if ('14' not in func_list) or ('15' not in func_list) or ('16' not in func_list):
                                show_member = 0

                            return  render(request, 'index.html',{'user_id': user_id,'name':name,'role':role,'department_id':department_id,'group_name':group_name,'depart_list':depart_list,'func_list':func_list,'show_depart':show_depart,'show_member':show_member})

                    else:
                        return render(request, 'user/login.html', {'msg': '登录页面', 'status': 0})
                except:
                    return render(request, 'user/login.html', {'msg': '登录页面', 'status': 0})
        elif request.method == 'POST':
            #POST
            domain_accounts = request.POST['domain_accounts']
            password = request.POST['password']
            objj = Users.objects.filter(domain_accounts = domain_accounts)

            obj = Users.objects.filter(domain_accounts = domain_accounts,password = password,deleted = 0)
            if obj.exists():
                if objj.values('group_id')[0]['group_id'] == 3:
                    return render(request, 'user/login.html', {'msg': '未分组，无法登陆', 'status': 1})
                user = obj.values('role_id','name','user_id','department_id','group_id','group_id__name','group_id__depart_list','group_id__func_list')[0]
                role = user['role_id']
                name = user['name']
                user_id = user['user_id']
                department_id = user['department_id']
                group_name = user['group_id__name']
                depart_list = user['group_id__depart_list'].split(',')
                func_list = user['group_id__func_list'].split(',')



                if role == 0:
                    msgCount = Message.objects.filter(is_read = 0,deleted = 0).count()
                    ret = render(request, 'index.html',
                                 {'status': 0, 'msg': '登录成功', 'user_id': user_id, 'name': name, 'role': role,
                                  'department_id': department_id,'msgCount':msgCount,'group_name':group_name,'depart_list':depart_list,'func_list':func_list,'show_depart':1,'show_member':1})
                else:
                    show_depart = 1
                    show_member = 1
                    if ('11' not in func_list) and ('12' not in func_list) and ('13' not in func_list):
                        show_depart = 0
                    if ('14' not in func_list) and  ('15' not in func_list) and  ('16' not in func_list):
                        show_member = 0
                    ret = render(request, 'index.html',
                                 {'status': 0, 'msg': '登录成功', 'user_id': user_id, 'name': name, 'role': role,
                                  'department_id': department_id,'group_name':group_name,'depart_list':depart_list,'func_list':func_list,'show_depart':show_depart,'show_member':show_member})
                content = "".join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890' + string.digits) for i in range(20)])
                userInfo = {'domain_accounts':domain_accounts,'user_id':user_id,'name':name,'role_id':role,'department_id':department_id,'group_name':group_name,'depart_list':depart_list,'func_list':func_list}
                ret.set_cookie('user',content,max_age=1*60*60*24)
                request.session[content] = userInfo
                request.session.set_expiry(1*60*60*24)
                # request.session.set_expiry(None)
                return ret
            else:
                return render(request,'user/login.html',{'msg':'账号或密码错误','status':1})


# 注销
    def logout(request):
        try:
            user = request.COOKIES['user']
            del request.session[user]
        except:
            pass
        return render(request, 'user/login.html', {'msg': '登录成功', 'status': 0})
# 修改密码
    def changePasswd(request):
        if request.method == 'GET':
            return render(request,'user/changePasswd.html')
        if request.method == 'POST':
            try:
                cookie_content = request.COOKIES
                user = cookie_content['user']
                userInfo = request.session[user]
                domain_accounts = userInfo['domain_accounts']
                role = userInfo['role_id']
                password = request.POST['password']
                client_domain_accounts = request.POST['domain_accounts']
                if (domain_accounts == client_domain_accounts) or (role ==0):
                    Users.objects.filter(domain_accounts=domain_accounts).update(password = password)
                    return render(request,'user/changePasswd.html',{'status':1,'msg':'你居然修改成功了？'})
                else:
                    return render(request, 'user/changePasswd.html', {'status': 0, 'msg': '修改其他人的密码干嘛？'})
            except:
                return render(request,'user/changePasswd.html',{'status':0,'msg':'修改失败'})
    #用户及部门管理
    def userManage(request):
        return render(request,'user/manage.html',status = 200)

    #用户增加表单
    def userAddForm(request):
        return render(request,'user/add.html',status = 200)

   #用户增加
    def userAdd(request):
        if request.method == 'get':
            return render(request,'user/member-add.html')
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                mobile = data['mobile']
                name = data['name']
                user_id = data['user_id']
                department = data['department']
                role = data['role']
                obj = Users.objects.filter(user_id = user_id,deleted = 0)

                if Users.objects.filter(user_id=user_id, deleted=1).exists():
                    Users.objects.filter(user_id=user_id).update(role_id=role, user_id=user_id, name=name,
                                                                 join_time=datetime.datetime.now(), mobile=mobile,
                                                                 department_id=department, status=1, deleted=0,
                                                                 group_id=3)
                    return JsonResponse({"msg": "成功更新员工"}, status=200)
                # if obj.exists():
                #     return JsonResponse({'msg':"此工号已存在"},status = 400)
                else:
                    # if Users.objects.filter(user_id = user_id,deleted = 1).exists():
                    #     Users.objects.filter(user_id = user_id).update(role_id=role, user_id=user_id, name=name, join_time=datetime.datetime.now(),mobile=mobile, department_id=department, status=1, deleted=0,group_id = 3)
                    #     return JsonResponse({"msg": "ok"}, status=200)
                    # else:
                    Users.objects.create(role_id=role, user_id=user_id, name=name, join_time=datetime.datetime.now(),mobile=mobile, department_id=department, status=1, deleted=0,password = '123456',group_id = 3)
                    return JsonResponse({"msg":"ok"},status=200)
            except:
                return JsonResponse({"msg":"fail"},status=400)

#删除用户
    def memberdel(request):
        res = Users.objects.filter(deleted=1).order_by('-leave_time')
        return render(request, 'member-del.html', {'user': res})

#显示用户
    def memberlist(request):
        userInfo = request.session[request.COOKIES['user']]
        role = userInfo['role_id']
        department_id = userInfo['department_id']
        if request.method == 'GET':
            if role == 0:
                res = Users.objects.filter().order_by('deleted','-id')[0:10]
                count = Users.objects.filter().count()
                return render(request, 'member-list.html',{'user':res,'count':count})
            else:
                res = Users.objects.filter(department_id = department_id).order_by('deleted', '-id')[0:10]
                count = Users.objects.filter(department_id = department_id).count()
                return render(request, 'member-list.html', {'user': res, 'count': count})


        if request.method == 'POST':
            id = request.POST['id'] - 1
            start = id * 10
            end = start + 10
            if role == 0:
                res = Users.objects.filter().order_by('deleted', '-id')[start:end]
                count = Users.objects.filter().count()
                return render(request, 'member-list.html', {'user': res, 'count': count})
            else:
                res = Users.objects.filter(department_id = department_id).order_by('deleted', '-id')[start:end]
                count = Users.objects.filter(department_id = department_id).count()
                return render(request, 'member-list.html', {'user': res, 'count': count})




    #获取用户信息
    def getUserInfoList(request):
        data = request.GET

        user = request.COOKIES['user']
        userInfo = request.session[user]
        status = Users.objects.filter(user_id=userInfo['user_id']).values('status')[0]['status']
        user_id = userInfo['user_id']
        if status == 0:
            userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
        depart_list = userInfo['depart_list']

        page = int(data.get('page'))
        limit = int(data.get('limit'))
        start = page*limit-limit
        end = page*limit


        if data.get('searchInfo'):
            searchInfo = data.get('searchInfo').replace(' ','')
            try:
                user = list(Users.objects.filter(Q(department_id__in = depart_list) & Q(deleted = 0)&(Q( user_id__icontains = searchInfo) | Q(name__icontains= searchInfo) | Q(seat_id__icontains=searchInfo)) ).values('id','name','age','seat_id','user_id','status','deleted','department_id__name','role__name','group_id__name').order_by('-id')[start:end])
                count = Users.objects.filter(Q(department_id__in = depart_list) & Q(deleted = 0)&(Q( user_id__icontains = searchInfo) | Q(name__icontains= searchInfo) | Q(seat_id__icontains=searchInfo)) ).count()
                return JsonResponse({"code": 0,"msg": "ok","count": count,"data": user})

            except:
                return JsonResponse({"code": 1,"msg": "fail","count":0,"data":''})
        else:
            try:
                user = list(Users.objects.filter(Q(department_id__in = depart_list)& Q(deleted = 0)).values('id','name','age','seat_id','user_id','status','deleted','department_id__name','role__name','group_id__name').order_by('-id')[start:end])
                count = Users.objects.filter(Q(department_id__in = depart_list)& Q(deleted = 0)).count()
                return JsonResponse({"code": 0,"msg": "ok","count": count,"data": user})
            except:
                return JsonResponse({"code": 1,"msg": "fail","count":0,"data":''})

#删除用户
    def delUser(request):

        data = json.loads(request.body)
        try:
            # userInfo = request.session[request.COOKIES['user']]
            user = request.COOKIES['user']
            userInfo = request.session[user]
            status = Users.objects.filter(user_id=userInfo['user_id']).values('status')[0]['status']
            user_id = userInfo['user_id']
            if status == 0:
                userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
            if '14' not in userInfo['func_list']:
                return JsonResponse({'msg': '沒有刪除權限'}, status=400)
            if data['title'] == 'delOneUser':
                id = data['id']
                se = Users.objects.filter(id=id).values('seat_id')[0]['seat_id']
                if se != None:
                    status = Seat.objects.filter(seat_id = se).values('status')[0]['status']
                    if status == 1:
                        status = 2
                    elif  status == 5:
                        status = 4
                    elif status == 8:
                        status = 7
                    Seat.objects.filter(seat_id = se).update(status = status)
                    # return JsonResponse({'msg': '请先取消工位'}, status=400)
                Users.objects.filter(id=id).update(deleted=1, leave_time=datetime.datetime.now(), seat_id=None)
                return JsonResponse({'msg': '刪除成功'}, status=200)
            elif data['title'] == 'delManyUser':
                id = data['id']
                u = []
                for ii in id:
                    if Users.objects.filter(id =  ii).values('seat_id')[0]['seat_id'] != None:
                        u.append(ii)
                if len(u) > 0:
                    return JsonResponse({'msg':'有人还占座呢'},status = 400)
                Users.objects.filter(id__in=id).update(deleted=1, leave_time=datetime.datetime.now(), seat_id=None)
                return JsonResponse({'msg': '批量刪除成功'}, status=200)
        except:
            return JsonResponse({'msg': '刪除失敗'}, status=400)

    def setUserRole(request):
        data = json.loads(request.body)
        try:
            id = data['id']
            role = data['role']
            Users.objects.filter(id = id).update(role_id = int(role))
            return JsonResponse({"code": 0, "msg":'successful', "count": 0, "data": ''}, status=200)

        except:
            return JsonResponse({"code": 1, "msg": 'fail', "count": 0, "data": ''}, status=200)



class DepartmentClass(View):


    def getDepartSolutionInfo(request):
        departObj = list(Department.objects.filter(Q(deleted = 0) & ~Q(id = 14)).values('name'))
        allDepart = {}
        for i in departObj:
            # allDepart[i['name']] = [{'value':0, 'name': '已使用'}, {'value': 0, 'name': '未使用'}]
            allDepart[i['name']] = [{'value':0, 'name': '已使用'}, {'value': 0, 'name': '未使用'}]

        seatObj = list(Seat.objects.filter(~Q(department_id = 14)).values('status','department_id__name'))
        for one in seatObj:
            status = one['status']
            name = one['department_id__name']
            used = allDepart[name][0]['value']
            noused = allDepart[name][1]['value']
            if status in [1,5,8]:
                allDepart[name][0]['value'] = allDepart[name][0]['value'] + 1

            elif status in [2,4,7]:
                allDepart[name][1]['value'] = allDepart[name][1]['value'] + 1




        return  JsonResponse({'departObj':departObj,'allDepart':allDepart,'msg':'success'},status = 200)





    def getDepartmentSeatInfo(request):



        depart = list(Department.objects.filter(deleted = 0).values('id','name'))
        obj = {}
        departList = []
        departName = []
        for one in depart:
            id = one['id']
            name = one['name']
            obj[id] = {'已使用':0,'未使用':0}
            if id != 14:
                departList.append(id)
                departName.append({'name':name, 'max': 10})
        seat = list(Seat.objects.filter(department_id__in = departList).values('department_id','status'))
        for i in seat:
            status = i['status']
            id = i['department_id']
            if status == 1:
                obj[id]['已使用'] += 1
            if status == 2:
                obj[id]['未使用'] += 1
        data = [
            {"value": [],"name": "已使用"},

            {"value": [], "name": "未使用"}
        ]
        for ii in obj:
            data[0]['value'].append(obj[ii]['已使用'])
            data[1]['value'].append(obj[ii]['未使用'])
        return JsonResponse({'data':data,'departName':departName},status = 200)



#获取部门
    def selectDepartment(request):
        #助理:使用,新增,申请 管理员:所有
        user = request.COOKIES['user']
        userInfo = request.session[user]
        # user_id == userInfo['user_id']
        user_id = userInfo['user_id']
        status = Users.objects.filter(user_id = userInfo['user_id']).values('status')[0]['status']
        if status == 0:
            userInfo = Admin.ChangeCookiesAndSession(request,user,user_id)
        depart_list = userInfo['depart_list']
        data = list(Department.objects.filter(Q(deleted = 0) & Q(id__in = depart_list) & ~Q(id = 14)).values('id','name').order_by('-id'))

        return JsonResponse({'department':data},status = 200)

        # 使用工位获取部门
    def selectDepartment1(request):
        data = json.loads(request.body)
        x = data['x']
        y = data['y']
        floor = data['floor']
        data = list(Seat.objects.filter(x= x ,y = y ,floor = floor).values('department_id__id','department_id__name'))
        # 获取此部门员工
        obj = list(Users.objects.filter(seat_id = None,department_id = data[0]['department_id__id'] ,deleted = 0).values('id','name'))
        return JsonResponse({'department': data,'obj':obj}, status=200)



    def departmentAddForm(request):
        return render(request, 'user/department-add.html', status = 200)

    def departmentEdit(request):
        if request.method == 'GET':
            return render(request, 'user/department-edit.html', status = 200)
        if request.method == 'POST':
            data = json.loads(request.body)
            name = data['name']
            id = data['id']
            try:
                user = request.COOKIES['user']
                userInfo = request.session[user]
                status = Users.objects.filter(user_id=userInfo['user_id']).values('status')[0]['status']
                user_id = userInfo['user_id']
                if status == 0:
                    userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
                if '12' not in userInfo['func_list']:
                    return JsonResponse({'msg': '无修改部门权限'}, status=400)
                Department.objects.filter(id=id).update(name=name)
                return JsonResponse({'msg': '修改成功'}, status=200)
            except:
                return JsonResponse({'msg': '修改失败'}, status=400)

    def addDepartment(request):
        data = json.loads(request.body)

        name = data['name']
        try:
            user = request.COOKIES['user']
            # 改变func_list
            userInfo = request.session[user]
            user_id = userInfo['user_id']
            status = Users.objects.filter(user_id=user_id).values('status')[0]['status']
            if status == 0:
                userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
            if '11' not in userInfo['func_list']:
                return JsonResponse({'msg': '无新增部门权限'}, status=400)
            obj = Department.objects.filter(name = name)
            if obj.exists():
                obj.update(name = name,deleted = 0)
            else:
                Department.objects.create(name = name,deleted = 0)
            return JsonResponse({'msg':'ok'},status = 200)
        except:
            return JsonResponse({'msg':'error'},status = 400)

    def delDepartment(request):
        data = json.loads(request.body)
        id = data['id']
        User = Users.objects.filter(department_id = id,deleted = 0)
        try:
            user = request.COOKIES['user']
            # 改变func_list
            userInfo = request.session[user]
            user_id = userInfo['user_id']
            status = Users.objects.filter(user_id=user_id).values('status')[0]['status']
            if status == 0:
                userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
            if '13' not in userInfo['func_list']:
                return JsonResponse({'msg': '无删除部门权限'}, status=400)

            if User.exists():
                return JsonResponse({'msg': '部門下有用戶,无法删除'}, status=400)
            else:
                Department.objects.filter(id = id).update(deleted = 1)
                return JsonResponse({'msg': '删除成功'}, status=200)
        except:
            return JsonResponse({'msg': '错误'}, status=400)

    def departmentList(request):
        return render(request,'department-list.html',status = 200)

    def getDepartmentInfo(request):
        data = request.GET


        try:
            page = int(data.get('page'))
            limit = int(data.get('limit'))
            start = page * limit - limit
            end = page * limit
            user = request.COOKIES['user']
            # 改变func_list
            userInfo = request.session[user]
            user_id = userInfo['user_id']
            status = Users.objects.filter(user_id=user_id).values('status')[0]['status']
            if status == 0:
                userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
            depart_list = userInfo['depart_list']
            obj = list(Department.objects.filter(Q(deleted=0) & ~Q(id =14) & Q(id__in = depart_list)).values().order_by('-id')[start:end])
            count = Department.objects.filter(Q(deleted=0) & ~Q(id =14)).count()
            return JsonResponse({"code": 0, "msg": "ok", "count": count, "data": obj})
        except:
            return JsonResponse({"code": 1, "msg": "fail", "count": 0, "data": ''})

class FloorClass(View):
    #获得每个楼层使用详情
    def emptySolution(request):
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        if Empty.objects.filter(time = now).exists():
            return JsonResponse({'error_msg': '当日已存在'})
        else:
            data = list(Seat.objects.filter().values('status', 'floor'))
            obj = {'35': [0, 0,0], '36': [0, 0,0], '37': [0, 0,0], '38': [0, 0,0], '39': [0, 0,0], '40': [0, 0,0], 'all': [0, 0,0], }
            for i in data:
                status = i['status']
                floor = i['floor']
                obj['all'][1] += 1
                obj[floor][1] += 1
                if status in [0, 3, 6]:
                    obj[floor][0] += 1
                    obj['all'][0] += 1
            for u in ['35','36','37','38','39','40','all']:
                obj[u][2] = obj[u][0]/obj[u][1]*100
            Empty.objects.create(all = obj['all'][2],zero=obj['40'][2],nine=obj['39'][2],eight=obj['38'][2],seven=obj['37'][2],six=obj['36'][2],five=obj['35'][2],time = now)
            return JsonResponse({'error_msg':'成功添加'})

    def getFloorInfo(request):
        res = list(Seat.objects.filter().values('floor','status'))
        obj = {
            '35':[{'value': 0, 'name': '已使用'}, {'value': 0, 'name': '未分配'}, {'value':0, 'name': '未使用'}],
            '36':[{'value': 0, 'name': '已使用'}, {'value': 0, 'name': '未分配'}, {'value':0, 'name': '未使用'}],
            '37':[{'value': 0, 'name': '已使用'}, {'value': 0, 'name': '未分配'}, {'value':0, 'name': '未使用'}],
            '38':[{'value': 0, 'name': '已使用'}, {'value': 0, 'name': '未分配'}, {'value':0, 'name': '未使用'}],
            '39':[{'value': 0, 'name': '已使用'}, {'value': 0, 'name': '未分配'}, {'value':0, 'name': '未使用'}],
            '40':[{'value': 0, 'name': '已使用'}, {'value': 0, 'name': '未分配'}, {'value':0, 'name': '未使用'}],
        }
        for i in res:
            floor = i['floor']
            status = i['status']
            if status == 1 or status == 5 or status == 8:
                obj[floor][0]['value'] += 1
            elif status == 0 or status == 3 or status == 6:
                obj[floor][1]['value'] += 1
            elif status == 2 or status == 4 or status == 7:
                obj[floor][2]['value'] += 1
        daydata = list(Empty.objects.all().values().order_by('time'))
        five,six,seven,eight,nine,zero,all= [],[],[],[],[],[],[]

        date = [(i['time'].strftime('%Y-%m-%d')) for i in daydata]
        # [(bili35.append(i['have']),all.append(i['all']),nohave.append(i['nohave'])) for i in daydata]
        [(five.append(i['five']),all.append(i['all']),six.append(i['six']),seven.append(i['seven']),eight.append(i['eight']),nine.append(i['nine']),zero.append(i['zero'])) for i in daydata]

        # return JsonResponse({'obj': obj,'date':date,'have':have,'nohave':nohave,'all':all},status = 200)
        return JsonResponse({'obj': obj,'date':date,'five':five,'six':six,'seven':seven,'eight':eight,'nine':nine,'zero':zero,'all':all},status = 200)

class RecordClass(View):
    def operateRecord(request):
        if request.method == 'GET':
            return render(request,'record/record.html')

    def getRecord(request):
        userInfo = request.session[request.COOKIES['user']]
        depart_list = userInfo['depart_list']
        if request.method == "GET":
            obj = list(Record.objects.filter(department_id__in = depart_list).values('id','user_id','name','department_id__name','record_time','action','seat_id').order_by('-id')[0:5])
            return JsonResponse({'obj':obj},status = 200)
        if request.method == 'POST':
            data = json.loads(request.body)
            if data['title'] == 'getLarge':
                id = data['uuid']
                obj = list(
                    Record.objects.filter(department_id__in=depart_list, id__gt=id).values('id', 'user_id', 'name',
                                                                                           'department_id__name',
                                                                                           'record_time', 'action',
                                                                                           'seat_id').order_by('-id'))
                return JsonResponse({'obj':obj},status = 200)

            else:
                id = data['uuid']
                obj = list(Record.objects.filter(department_id__in = depart_list,id__lt = id).values('id','user_id','name','department_id__name','record_time','action','seat_id').order_by('-id')[0:5])
                return JsonResponse({'obj':obj},status = 200)



class SeatClass(View):

    def getSeatInfo(request):
        data = request.GET
        user = request.COOKIES['user']
        userInfo = request.session[user]
        status = Users.objects.filter(user_id=userInfo['user_id']).values('status')[0]['status']
        user_id = userInfo['user_id']
        typeInfo = {'0': '标准工位', '1': '主管工位', '2': '办公室'}
        statusInfo = {'0': '未分配', '1': '已使用', '2': '未使用', '3': '未分配', '4': '未使用', '5': '已使用', '6': '未分配', '7': '未使用',
                      '8': '已使用'}
        if status == 0:
            userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
        depart_list = userInfo['depart_list']

        page = int(data.get('page'))
        limit = int(data.get('limit'))
        start = page*limit-limit
        end = page*limit

        if data.get('searchInfo'):
            searchInfo = data.get('searchInfo').replace(' ', '')


            try:
                seatList = list(
                    Seat.objects.filter(Q(department_id__in=depart_list)  &
                       Q(
                        seat_id__icontains=searchInfo) ).values('seat_id', 'floor', 'type',
                                                                              'status', 'department_id__name'))
                userinfo = list(Users.objects.filter(Q(department_id__in=depart_list) & Q(deleted=0) & (
                            Q(user_id__icontains=searchInfo) | Q(name__icontains=searchInfo) | Q(
                        seat_id__icontains=searchInfo))).values('seat_id', 'name', 'user_id'))
                dic = {}
                for u in userinfo:
                    dic[u['seat_id']] = {'user_id': u['user_id'], 'name': u['name']}
                # print(dic)
                for i in seatList:
                    try:
                        i['status__status'] = statusInfo[str(i['status'])]
                        i['type__type'] = typeInfo[str(i['type'])]
                        s = dic[i['seat_id']]
                        i['name'] = s['name']
                        i['user_id'] = s['user_id']
                    except Exception as e:
                        continue
                count = len(seatList)
                return JsonResponse({"code": 0, "msg": "ok", "count": count, "data": seatList})
            except:
                return JsonResponse({"code": 1, "msg": "fail", "count": 0, "data": ''})
        else:
            try:
                seatList = list(Seat.objects.filter(department_id__in = depart_list).values('seat_id','floor','type','status','department_id__name')[start:end])
                userinfo = list(Users.objects.filter(Q(department_id__in=depart_list) & Q(deleted=0)).values('seat_id','name', 'user_id'))
                dic = {}
                for u in userinfo:
                    dic[u['seat_id']] = {'user_id':u['user_id'],'name':u['name']}
                # print(dic)
                for i in seatList:
                    try:
                        i['status__status'] = statusInfo[str(i['status'])]
                        i['type__type'] = typeInfo[str(i['type'])]
                        s = dic[i['seat_id']]
                        i['name'] = s['name']
                        i['user_id'] = s['user_id']
                    except Exception as e:
                        continue
                # print(seatList[10])
                # user = list(Users.objects.filter(Q(department_id__in = depart_list)& Q(deleted = 0)).values('id','name','age','seat_id','user_id','status','deleted','department_id__name','role__name','group_id__name').order_by('-id')[start:end])
                count = Seat.objects.filter(Q(department_id__in = depart_list)).count()
                return JsonResponse({"code": 0,"msg": "ok","count": count,"data": seatList})
            except:
                return JsonResponse({"code": 1,"msg": "fail","count":0,"data":''})


    def seatInfo(request):

        return render(request,'seat/seatInfo.html',status =200)


    def analysis(request,name,user_id,role,department_id):

        userInfo = request.session[request.COOKIES['user']]
        user = request.COOKIES['user']
        userInfo = request.session[user]
        status = Users.objects.filter(user_id=userInfo['user_id']).values('status')[0]['status']
        user_id = userInfo['user_id']
        if status == 0:
            userInfo = Admin.ChangeCookiesAndSession(request, user, user_id)
        func_list = userInfo['func_list']
        if '10' not in func_list:
            return redirect('/seatSystem/seatChoice/')
        #员工数
        UserCount = Users.objects.filter(deleted = 0).count()
        #总工位
        count = Seat.objects.count()
        #未分配工位
        leftSeat = Seat.objects.filter(Q(status = 0) | Q(status = 3 ) | Q(status = 6)).count()
        #部门申请未使用
        waitSeat = Seat.objects.filter(Q(status = 2) | Q(status = 4 ) | Q(status = 7)).count()
        #部门申请已使用
        usedSeat = Seat.objects.filter(Q(status = 1) | Q(status = 5 ) | Q(status = 8)).count()
        #工位种类
        #主管工位
        managedSeat = Seat.objects.filter(type = 1).count()
        #标准工位
        standardSeat = Seat.objects.filter(type = 0).count()

        #办公室工位
        officeSeat = Seat.objects.filter(type = 2).count()
        #工位利用率
        usedSeatbili = str(((usedSeat+waitSeat) / count) * 100)[0:4]
        return render(request,'seat/analysis.html',{'seatInfo':[count,leftSeat,waitSeat,usedSeat,managedSeat,standardSeat,usedSeatbili,officeSeat],'userInfo':[UserCount,name,user_id,role,department_id]})


    def seatChoice(request):
        userInfo = request.session[request.COOKIES['user']]
        depart_list = userInfo['depart_list']
        res = Seat.objects.filter(department_id__in=depart_list).values('seat_id', 'status', 'floor', 'type')
        result = {}
        for i in ['35', '36', '37', '38', '39', '40']:
            result[i] = {'seatcount': 0, 'have': 0, 'nohave': 0, 'wait': 0}
        role = request.session[request.COOKIES['user']]['role_id']
        count = 0
        for one in res:
            status = one['status']
            floor = str(one['floor'])
            if floor in result:
                count += 1
                allseat = result[floor]['seatcount']
                have = result[floor]['have']
                nohave = result[floor]['nohave']
                wait = result[floor]['wait']
                if status == 1:
                    result[floor]['seatcount'] = allseat + 1
                    result[floor]['have'] = have + 1
                elif status == 2:
                    result[floor]['seatcount'] = allseat + 1
                    result[floor]['nohave'] = nohave + 1
                elif status == 0:
                    result[floor]['seatcount'] = allseat + 1
                    result[floor]['wait'] = wait + 1

                elif status == 3:
                    result[floor]['seatcount'] = allseat + 1
                    result[floor]['wait'] = wait + 1
                elif status == 4:
                    result[floor]['seatcount'] = allseat + 1
                    result[floor]['nohave'] = nohave + 1
                elif status == 5:
                    result[floor]['seatcount'] = allseat + 1
                    result[floor]['have'] = have + 1
                elif status == 6:
                    result[floor]['seatcount'] = allseat + 1
                    result[floor]['wait'] = wait + 1
                elif status == 7:
                    result[floor]['seatcount'] = allseat + 1
                    result[floor]['nohave'] = nohave + 1
                elif status == 8:
                    result[floor]['seatcount'] = allseat + 1
                    result[floor]['have'] = have + 1
            #
            # else:
            #     count += 1
            #     if status == 1:
            #         result[floor] = {'seatcount': 1, 'have': 1, 'nohave': 0, 'wait': 0}
            #     elif status == 2:
            #         result[floor] = {'seatcount': 1, 'have': 0, 'nohave': 1, 'wait': 0}
            #     elif status == 0:
            #         result[floor] = {'seatcount': 1, 'have': 0, 'nohave': 0, 'wait':1}
        obj = []
        for one in result:
            if result[one]['seatcount'] != 0:
                bili = ((result[one]['have'] + result[one]['nohave']) / result[one]['seatcount'] )* 100

                bili = '' + str(bili)[0:4] + '%'
            else:
                bili = '0.0%'
            if (result[one]['seatcount'] != 0) or (result[one]['have'] != 0) or (result[one]['nohave'] != 0) or (
                    result[one]['wait'] != 0):
                oneFloor = {'floor': one, 'seatcount': result[one]['seatcount'], 'have': result[one]['have'],
                            'nohave': result[one]['nohave'], 'wait': result[one]['wait'], 'bili': bili}
                obj.append(oneFloor)

        obj = sorted(obj, key=lambda x: x["floor"])
        return render(request, 'seat/seatChoice.html', {'floor': obj, 'role': role, 'count': count})


    def addOneSeat(request):
        data = json.loads(request.body)
        try:
            x = data['x']
            y = data['y']
            floor = data['floor']
            seat_id = data['seat_id']
            Seat.objects.create(seat_id = seat_id,x = x ,y = y ,floor = floor,status = 0,department_id=14)
            return JsonResponse({'msg': '添加成功'}, status=200)
        except:
            return JsonResponse({'msg': '添加失败'}, status=400)


    def searchSeat(request):
        data = json.loads(request.body)
        try:
            seat_id = data['searchInfo']
            obj = Seat.objects.filter(seat_id = seat_id)
            seat = Users.objects.filter(name=seat_id)
            uid = Users.objects.filter(user_id=seat_id)
            if obj.exists():
                value = list(obj.values('x','y','floor'))
                return JsonResponse({'obj':value},status = 200)
            elif seat.exists():
                value = seat.values('seat_id')[0]['seat_id']
                if value:
                    value = list(Seat.objects.filter(seat_id=value).values('x', 'y', 'floor'))
                    return JsonResponse({'obj': value}, status=200)
                else:
                    return JsonResponse({'msg':'此人还未分配座位'},status = 400)
            elif uid.exists():
                value = uid.values('seat_id')[0]['seat_id']
                if value:
                    value = list(Seat.objects.filter(seat_id=value).values('x', 'y', 'floor'))
                    return JsonResponse({'obj': value}, status=200)
                else:
                    return JsonResponse({'msg': '此人还未分配座位'}, status=400)
            else:
                return JsonResponse({'msg':'工位不存在'},status = 400)

        except:
            return JsonResponse({'msg':'錯誤'},status = 400)

    def delForm(request):
        return render(request,'seat/del.html',status = 200)


    def lotzhipaiSeat(request):
        if request.method == 'GET':
            return render(request,'seat/lotzhipai.html',status= 200)

    def lotChangeSeat(request):
        data = json.loads(request.body)
        try:
            seatObj = []
            selectList = data['selectList']
            department_id = data['department_id']
            for one in selectList:
                obj = Seat.objects.filter(x = one['x'],y = one['y'],floor = one['floor'])
                obj.update(department_id = department_id,status = 2)
                seat = obj.values('seat_id')[0]['seat_id']
                seatObj.append(seat)

            userInfo = request.session[request.COOKIES['user']]
            user_id = userInfo['user_id']
            name = userInfo['name']
            department = userInfo['department_id']

            Record.objects.create(type=8, user_id=user_id, name=name, department_id=department, seat_id=seatObj,
                                  record_time=datetime.datetime.now(), deleted=0, action='批量指派工位')

            return JsonResponse({'msg':'success'},status = 200)

        except:
            return JsonResponse({'msg':'fail'},status = 400)

    def addSeat(request):
        if request.method == 'GET':
            return render(request,'seat/add.html',status= 200)
        if request.method == 'POST':
            data = json.loads(request.body)
            try:
                x = data['x']
                y = data['y']
                floor = data['floor']
                seat_id = data['seat_id']
                type = int(data['type'])
                obj = Seat.objects.filter(seat_id = seat_id)
                if obj.exists():
                    return JsonResponse({'msg':'工位号已存在'},status = 400)
                else:
                    userInfo = request.session[request.COOKIES['user']]
                    user_id = userInfo['user_id']
                    name = userInfo['name']
                    department = userInfo['department_id']
                    if type == 1:
                        #判断位置够不够
                        # 2位
                        for i in [0,1]:
                            for j in [0,1]:
                                if i == 0 and j == 0 :
                                    continue
                                else:
                                    if Seat.objects.filter(x = x+i , y = y+j , floor = floor).exists():
                                        return JsonResponse({'msg':'地方不够建主管座位'},status = 400)
                        Seat.objects.create(seat_id=seat_id, x=x, y=y, floor=floor, status=3, type=type,department_id=14)
                    elif type == 2:
                        for i in [0, 1, 2,3]:
                            for j in [0, 1, 2,3]:
                                if i == 0 and j == 0:
                                    continue
                                else:
                                    if Seat.objects.filter(x=x+i, y=y+j, floor=floor).exists():
                                        return JsonResponse({'msg': '地方不够建办公室'}, status=400)
                        Seat.objects.create(seat_id=seat_id, x=x, y=y, floor=floor, status=6, type=type,department_id=14)
                    elif type == 0:
                        Seat.objects.create(seat_id = seat_id , x = x , y = y ,floor = floor , status = 0,type = 0,department_id= 14)
                    Record.objects.create(type =1,user_id = user_id , name = name ,department_id = department,seat_id = seat_id ,record_time = datetime.datetime.now(),deleted = 0,action = '新增工位')
                    return JsonResponse({'msg':'新增成功'},status = 200)
            except Exception as e:
                return JsonResponse({'msg':'错误'},status = 400)
    def getSeatId(request):
        data = json.loads(request.body)
        x = data['x']
        y = data['y']
        floor = data['floor']
        seat_id = Seat.objects.filter(floor = floor ,x = x , y = y ).values('seat_id')[0]['seat_id']
        return JsonResponse({'obj':seat_id},status = 200)
    def zhipaiSeat(request):
        if request.method == 'GET':
            return render(request,'seat/zhipai.html',status = 200)
        if request.method == 'POST':
            data = json.loads(request.body)
            try:
                seat_id = data['seat_id']
                department_id = data['department_id']
                status = Seat.objects.filter(seat_id = seat_id).values('status')[0]['status']
                userInfo = request.session[request.COOKIES['user']]
                user_id = userInfo['user_id']
                name = userInfo['name']
                department = userInfo['department_id']


                if status  == 0:
                    Seat.objects.filter(seat_id = seat_id ).update(department_id = department_id,status = 2)
                    Record.objects.create(type=9, user_id=user_id, name=name, department_id=department, seat_id=seat_id,
                                          record_time=datetime.datetime.now(), deleted=0, action='指派工位')
                    return JsonResponse({'msg':'2'},status = 200)
                elif status == 3:
                    Seat.objects.filter(seat_id=seat_id).update(department_id=department_id, status=4)
                    Record.objects.create(type=9, user_id=user_id, name=name, department_id=department, seat_id=seat_id,
                                          record_time=datetime.datetime.now(), deleted=0, action='指派工位')
                    return JsonResponse({'msg': '4'}, status=200)
                elif status == 6:
                    Seat.objects.filter(seat_id=seat_id).update(department_id=department_id, status=7)
                    Record.objects.create(type=9, user_id=user_id, name=name, department_id=department, seat_id=seat_id,
                                          record_time=datetime.datetime.now(), deleted=0, action='指派工位')
                    return JsonResponse({'msg': '7'}, status=200)
                else:
                    return JsonResponse({'msg': '仅可指派未分配座位'}, status=400)

            except:
                return JsonResponse({'msg': 'fail'}, status=400)



    def systemBackSeat(request):
        id = json.loads(request.body)['id']
        try:
            seat_id = Message.objects.filter(id = id).values('seat_id')[0]['seat_id']
            Seat.objects.filter(seat_id = seat_id).update(department_id = 14,status = 0)
            return JsonResponse({'msg':'successful'},status = 200)
        except:
            return JsonResponse({'msg':'fail'},status = 400)

    def applicationForm(request):
        return render(request,'seat/application.html')

    def seatApplicationAction(request):
        data = json.loads(request.body)
        try:
            count = data['count']
            department_id = data['department_id']
            send_msg = data['send_msg']
            userInfo = request.session[request.COOKIES['user']]
            user_id = userInfo['user_id']
            name = userInfo['name']
            department = userInfo['department_id']
            msg = "您好，\n\n     您有一条来自%s的工位申请信息，请登陆工位管理系统进行处理。\n\n     登陆链接：http://seat.iflytek.com/seatSystem" % (name)
            receive_email = 'dfxie@iflytek.com'
            res = message.sendEmail(name, receive_email, msg)
            if res.status_code == 200:
                department_name = Department.objects.filter(id = department_id).values('name')[0]['name']
                # title = '员工%s为部门：%s申请工位,申请理由：%s' % (user_id, name,department_name,send_msg)
                title = '员工%s为%s部门申请工位%s个。请点击查看浏览详细内容。' %(name,department_name,count)
                send_time = datetime.datetime.now()
                Message.objects.create(send_user_id=user_id, receive_user_email=receive_email,
                                       send_status=1, title = title , send_msg=send_msg, is_read=0, is_pass=0, send_time=send_time,
                                       type='申请工位',count = count,deleted =0)
                Record.objects.create(type=4, user_id=user_id, name=name, department_id=department, seat_id=count,
                                      record_time=datetime.datetime.now(), deleted=0, action='申请工位')
                return JsonResponse({'msg': '已发起申请，请等待管理员审核'})
            else:
                return JsonResponse({'msg': '发起失败，请重试'})
        except:
            return JsonResponse({'msg': '发起失败，请重试'})







    # def getSeat(request):
    #     data = json.loads(request.body)
    #     try:
    #         floor = data['floor']
    #         department_id = data['department_id']
    #         if department_id == 0:
    #             position = list(Seat.objects.filter(floor=floor).values('x', 'y', 'status'))
    #             return JsonResponse({'position': position}, status=200)
    #         else:
    #             position = list(Seat.objects.filter(Q(floor=floor) & Q(department_id = department_id) & ~Q(status = 0)).values('x', 'y', 'status'))
    #             return JsonResponse({'position': position}, status=200)
    #     except:
    #         return JsonResponse({'msg': 'fail'}, status=200)

    def getSeat(request):
        data = json.loads(request.body)
        try:
            cookies = request.COOKIES
            userInfo = request.session[cookies['user']]
            group_name =userInfo['group_name']
            func_list = userInfo['func_list']
            depart_list = userInfo['depart_list']
            floor = data['floor']
            department_id = data['department_id']
            position = list(Seat.objects.filter(floor=floor,department_id__in = depart_list).values('x', 'y', 'status'))
            return JsonResponse({'position': position,'func_list':func_list}, status=200)
        except:
            return JsonResponse({'msg': 'fail'}, status=200)


    def seatAdd(request,floor):
        user = request.COOKIES['user']
        # 改变func_list
        userInfo = request.session[user]
        user_id = userInfo['user_id']
        status = Users.objects.filter(user_id = user_id).values('status')[0]['status']
        if status == 0:
            userInfo = Admin.ChangeCookiesAndSession(request,user,user_id)
            #改变状态为0
            # 改变session
        # userInfo = request.session[user]
        role = userInfo['role_id']
        department_id = userInfo['department_id']
        func_list = userInfo['func_list']
        depart_list = userInfo['depart_list']
        if 'search' in floor:
            list = floor.split('=')
            return render(request, 'seat/operate.html',{'floor': list[1], 'role': role, 'department_id': department_id, 'func_list': func_list,'depart_list': depart_list,'xx':list[2],'yy':list[3]})
        return render(request,'seat/operate.html',{'floor':floor,'role':role,'department_id':department_id,'func_list':func_list,'depart_list':depart_list})


    def chooseSeat(request):
        data = json.loads(request.body)
        x = data['x']
        y = data['y']

        floor = data['floor']
        Seat.objects.create(x = x ,y = y , floor = floor,choosed = 1)

        return JsonResponse({'msg':'选择成功'},status = 200)

#取消使用座位，变为未使用
    def noUserSeat(request):
        data = json.loads(request.body)
        try:
            num = 0
            x = data['x']
            y = data['y']
            floor = data['floor']
            obj = Seat.objects.filter(x = x ,y = y ,floor = floor)
            status = obj.values('status')[0]['status']
            if status == 1:
                num = 2
                obj.update(status = num)
            elif status == 5:
                num = 4
                obj.update(status = num)
            elif status == 8:
                num = 7
                obj.update(status = num)
            else:
                return JsonResponse({'msg':'仅可取消已使用座位'},status = 400)
            seat_id = obj.values('seat_id')[0]['seat_id']
            Users.objects.filter(seat_id = seat_id).update(seat_id = None)
            userInfo = request.session[request.COOKIES['user']]
            user_id = userInfo['user_id']
            name = userInfo['name']
            department = userInfo['department_id']
            Record.objects.create(type=6, user_id=user_id, name=name, department_id=department, seat_id=seat_id,
                                  record_time=datetime.datetime.now(), deleted=0, action='取消使用工位')
            return JsonResponse({'msg':'取消成功','obj':num},status = 200)
        except:
            return JsonResponse({'msg':'取消失败'},status = 400)


    def useSeatForm(request):
        return render(request,'seat/use.html',status = 200)

    def useSeat(request):
        data = json.loads(request.body)
        seat_id = data['seat_id']
        id = data['id']
        department_id = data['department_id']
        objj = Seat.objects.filter(seat_id = seat_id)
        # 如果座位的人存在，提示请先取消使用
        status = objj.values('status')[0]['status']
        Us = Users.objects.filter(id=id)
        userInfo = request.session[request.COOKIES['user']]
        user_id = userInfo['user_id']
        name = userInfo['name']
        department = userInfo['department_id']
        if status == 2:
            objj.update(status=1, department_id=department_id)
            Us.update(seat_id=seat_id)
            Record.objects.create(type=7, user_id=user_id, name=name, department_id=department, seat_id=seat_id,
                                  record_time=datetime.datetime.now(), deleted=0, action='使用工位')
            return JsonResponse({'msg': '成功使用标准座位','obj':1}, status=200)
        elif status == 4:
            objj.update(status=5, department_id=department_id)
            Us.update(seat_id=seat_id)
            Record.objects.create(type=7, user_id=user_id, name=name, department_id=department, seat_id=seat_id,
                                  record_time=datetime.datetime.now(), deleted=0, action='使用工位')
            return JsonResponse({'msg': '成功使用主管座位', 'obj': 5}, status=200)
        elif status == 7:
            objj.update(status=8, department_id=department_id)
            Us.update(seat_id=seat_id)
            Record.objects.create(type=7, user_id=user_id, name=name, department_id=department, seat_id=seat_id,
                                  record_time=datetime.datetime.now(), deleted=0, action='使用工位')
            return JsonResponse({'msg': '成功使用办公司座位', 'obj': 8}, status=200)
        else:
            return JsonResponse({'msg': '只有未使用才能使用！'}, status=400)
        # obj = Users.objects.filter(id= id)
        # # 有这人就更新座位，没这人就创建人
        # if obj.exists():
        #     Seat.objects.filter(seat_id=seat_id).update(status=1,department_id = department_id)
        #     Users.objects.filter(id = id ).update(seat_id = seat_id)
        #     return JsonResponse({'msg':'成功更新座位'},status = 200)

    def getUserSeatId(request):
        data = json.loads(request.body)
        x = data['x']
        y = data['y']
        floor = data['floor']
        info = Seat.objects.filter(floor = floor ,x = x ,y = y ).values('seat_id')[0]
        return JsonResponse({'info':info},status = 200)

    def getUserIdSuggestion(request):
        user_id = json.loads(request.body)['user_id']
        user = request.COOKIES['user']
        userInfo = request.session[user]
        department_id = userInfo['department_id']
        info = list(Users.objects.filter(department_id = department_id  ,user_id__icontains= user_id).order_by('-id').values('user_id','name')[0:4])
        return JsonResponse({'info':info},status = 200)

# 助理退回工位，审核
    def backSeat(request):
        data = json.loads(request.body)
        x = data['x']
        y = data['y']
        floor = data['floor']
        obj = Seat.objects.filter(floor = floor ,x = x , y = y )
        try:
            if obj.values('status')[0]['status'] not in [2,4,7]:
                return JsonResponse({'msg':'仅可退还未分配座位'},status = 400)
            else:
                #发送邮件 座位号+楼层
                seat_id = obj.values('seat_id')[0]['seat_id']
                #发送邮件
                cookie_content = request.COOKIES
                user = cookie_content['user']
                userInfo = request.session[user]
                name= userInfo['name']
                user_id = userInfo['user_id']
                department = userInfo['department_id']
                # title = '退还工位:%s' %(seat_id)
                msg = "您好，\n\n     您有一条来自%s的退还工位信息，请登陆工位管理系统进行处理。\n\n     登陆链接：http://seat.iflytek.com/seatSystem" %(name)
                # receive_email = 'guqiankun@hotmail.com'
                receive_email = 'dfxie@iflytek.com'
                res = message.sendEmail(name,receive_email,msg)
                if res.status_code == 200:
                    title = '员工%s申请退还工位。请点击查看浏览详细内容。' %(name)
                    send_msg = '退还工位'
                    send_time = datetime.datetime.now()
                    Message.objects.create(deleted = 0 ,send_user_id = user_id , receive_user_email = receive_email,title = title, seat_id = seat_id , send_status = 1,send_msg = send_msg ,is_read = 0 ,is_pass = 0 ,send_time = send_time,type = '退还工位')
                    Record.objects.create(type = 3 , user_id = user_id ,name = name ,department_id = department ,seat_id = seat_id ,record_time = datetime.datetime.now(),deleted = 0 ,action = '退还工位')
                    return JsonResponse({'msg':'成功申请退还工位，请等待管理员审核'})
                else:
                    return JsonResponse({'msg': '邮件未发送，请重试'}, status=400)
        except:
            return JsonResponse({'msg':'退还失败，请重试'},status = 400)

#管理员删除工位
    def delSeat(request):
        data = json.loads(request.body)
        try:
            x = data['x']
            y = data['y']
            floor = data['floor']
            obj = Seat.objects.filter(floor = floor , x = x , y = y)
            status = obj.values('status')[0]['status']
            if status  in [0,3,6]:
                seat_id = obj.values('seat_id')[0]['seat_id']
                obj.delete()
                Users.objects.filter(seat_id = seat_id).update(seat_id = None)
                userInfo = request.session[request.COOKIES['user']]
                user_id = userInfo['user_id']
                name = userInfo['name']
                department = userInfo['department_id']
                Record.objects.create(type = 2,user_id = user_id , name = name ,department_id = department,seat_id = seat_id,record_time = datetime.datetime.now(),deleted = 0 ,action = '删除座位' )
                return JsonResponse({'msg':'删除成功'},status = 200)
            else:
                return JsonResponse({'msg': '仅可删除未分配座位'}, status=400)
        except:
            return JsonResponse({'msg':'删除失败'},status = 400)
#管理员回收工位
    def recycleSeat(request):
        data = json.loads(request.body)
        x = data['x']
        y = data['y']
        floor = data['floor']
        obj = Seat.objects.filter(floor=floor, x=x, y=y)
        try:
            num = 100
            status = obj.values('status')[0]['status']
            if  status == 2:
                num = 0
                obj.update(status=num, department_id=14)
            elif status == 4:
                num = 3
                obj.update(status=num, department_id=14)
            elif status == 7:
                num = 6
                obj.update(status=num, department_id=14)
            else:
                return JsonResponse({'msg': '仅可回收已分配未使用座位'}, status=400)
            seat_id = obj.values('seat_id')[0]['seat_id']
            Users.objects.filter(seat_id=seat_id).update(seat_id="")
            userInfo = request.session[request.COOKIES['user']]
            user_id = userInfo['user_id']
            name = userInfo['name']
            department = userInfo['department_id']
            Record.objects.create(type=5, user_id=user_id, name=name, department_id=department, seat_id=seat_id,
                                  record_time=datetime.datetime.now(), deleted=0, action='回收工位')

            return JsonResponse({'msg': '回收成功','obj':num}, status=200)
        except:
            return JsonResponse({'msg': '回收失败'}, status=400)


    def getUserInfoBySeat(request):
        data = json.loads(request.body)
        title = data['title']
        x = data['x']
        y = data['y']
        floor = data['floor']
        if title == 'used':
            seat_id = Seat.objects.filter(x=x, y=y, floor=floor).values('seat_id')[0]['seat_id']
            info = list(Users.objects.filter(seat_id = seat_id).values("user_id","department_id__name","seat_id","name"))
            info[0]['status'] = '已使用'
            return JsonResponse({'info':info},status = 200)
        elif title == 'noUsed':
            info = list(Seat.objects.filter(x=x, y=y, floor=floor).values('seat_id','department_id__name'))
            info[0]['status'] = '待使用'
            return JsonResponse({'info': info}, status=200)
        elif title == 'nobody':
            info = list(Seat.objects.filter(x=x, y=y, floor=floor).values('seat_id'))
            info[0]['status'] = '未分配'
            return JsonResponse({'info': info}, status=200)


    def test(request):
        from django.shortcuts import HttpResponse, render, redirect
        return redirect("http://www.baidu.com")

    #首页部门工位统计
    def getDepartmentSolutionInfo(request):
        departObj = list(Department.objects.filter(~Q(id = 14)&Q(deleted = 0)).values('id','name'))
        used = []
        nobody = []
        depart = []
        for i in departObj:
            used.append(Seat.objects.filter(department_id=i['id'],status__in = [1,5,8]).count())
            nobody.append(Seat.objects.filter(department_id=i['id'],status__in = [2,4,7]).count())
            depart.append(i['name'])
        return JsonResponse({'msg':'ok','data':[used,nobody,depart]})





