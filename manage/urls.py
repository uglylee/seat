# _*_ coding: utf-8 _*_
"""bdp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from manage import views as v
from manage import models as m
from django.urls import path
# from django.views import *

from django.conf.urls import url
urlpatterns = [

    # UserClass
    # 登录
    path('seatSystem/', v.UserClass.loginCheck, name='seatSystem'),
    path('seatSystem', v.UserClass.loginCheck, name='seatSystem'),
    # 注销
    path('seatSystem/logout/', v.UserClass.logout, name='logout'),
    # 新增用户
    path('seatSystem/userAdd', v.UserClass.userAdd, name='userAdd'),
    path('seatSystem/member-list/member-add/', v.UserClass.memberadd, name='addUser'),

    # 修改密码
    path('seatSystem/changePasswd/', v.UserClass.changePasswd, name='changePasswd'),
    # 统计
    path('seatSystem/welcome/<name>/<user_id>/<role>/<department_id>/', v.SeatClass.analysis, name='welcome'),
    # 用户管理
    path('seatSystem/member-list/', v.UserClass.memberlist, name='member-list'),
    # 编辑用户
    path('seatSystem/editUser/', v.UserClass.editUser, name='editUser'),
    # 删除用户
    path('seatSystem/member-del/', v.UserClass.memberdel, name='member-del'),

    #SeatClass
    path('seatSystem/addOneSeat/', v.SeatClass.addOneSeat, name='addOneSeat'),
    path('seatSystem/seatChoice/', v.SeatClass.seatChoice,name = 'seatChoice'),


    path('seatSystem/unicode/',v.index.unicode,name = 'unicode'),
    #Y用戶新增

    path('seatSystem/member-list/member-password/',v.Members.memberpassword,name = 'member-password'),
    path('seatSystem/admin-list/',v.Members.adminlist,name = 'admin-list'),
    path('seatSystem/admin-role/',v.Admin.adminrole,name = 'admin-role'),
    path('seatSystem/admin-rule/',v.Members.adminrule,name = 'admin-rule'),
    path('seatSystem/admin-cate/',v.Members.admincate,name = 'admin-cate'),
    path('seatSystem/admin-edit/', v.Admin.adminEdit, name='admin-edit'),

    path('seatSystem/editRole/<id>/',v.Admin.editRole,name = 'editRole'),

    path('seatSystem/changeGroupFunc/', v.Admin.changeGroupFunc, name='changeGroupFunc'),

    path('seatSystem/changeGroupDepart/', v.Admin.changeGroupDepart, name='changeGroupDepart'),
    #message
    path('seatSystem/sendMessageToAdmin/',v.message.sendMessageToAdmin,name = 'sendMessageToAdmin'),
    path('seatSystem/agreeMessage/',v.message.agreeMessage,name='agreeMessage'),
    path('seatSystem/writeSuggestion/',v.message.writeSuggestion,name='writeSuggestion'),
    path('seatSystem/changeSendMsg/', v.message.changeSendMsg, name='changeSendMsg'),
    path('seatSystem/contextMenuTest/',v.index.contextMenuTest,name = 'contextMenuText'),


    #获得用户信息
    path('seatSystem/getUserInfoList',v.UserClass.getUserInfoList,name= 'getUserInfoList'),
#获取分组信息
    path('seatSystem/setGroup/', v.Admin.setGroup, name='setGroup'),

    #删除用户
    path('seatSystem/member-list/delUser/', v.UserClass.delUser, name='delUser'),
    #设置角色
    path('seatSystem/setUserRole/',v.UserClass.setUserRole,name = 'setUserRole'),

#分组

    path('seatSystem/groupAdd/', v.Admin.groupAdd, name='group-add'),

    path('seatSystem/changeGroup/', v.Admin.changeGroup, name='changeGroup'),

    #部门

    path('seatSystem/departmentAddForm/', v.DepartmentClass.departmentAddForm, name='departmentAddForm'),
    path('seatSystem/departmentEdit/', v.DepartmentClass.departmentEdit, name='departmentEdit'),

    path('seatSystem/getDepartmentInfo/', v.DepartmentClass.getDepartmentInfo, name='getDepartmentInfo'),
    path('seatSystem/departmentList/', v.DepartmentClass.departmentList, name='department-list'),
    path('seatSystem/addDepartment/', v.DepartmentClass.addDepartment, name='addDepartment'),
    # path('seatSystem/editDepartment/', v.DepartmentClass.editDepartment, name='editDepartment'),
    path('seatSystem/delDepartment/', v.DepartmentClass.delDepartment, name='delDepartment'),

    path('seatSystem/selectDepartment',v.DepartmentClass.selectDepartment,name = 'selectDepartment'),
    path('seatSystem/selectDepartment1', v.DepartmentClass.selectDepartment1, name='selectDepartment1'),

    #用户a
    path('seatSystem/userManage/',v.UserClass.userManage,name='user-manage'),
    # path('seatSystem/userAdd/', v.UserClass.userAdd, name='userAdd'),

    #楼层
    path('seatSystem/getFloorInfo/', v.FloorClass.getFloorInfo, name='getFloorInfo'),


    #工位
    path('seatSystem/seatApplicationForm/', v.SeatClass.applicationForm, name='seatApplication'),
        #排座跳转
        path('seatSystem/seatChoice/seat-add/<floor>/', v.SeatClass.seatAdd, name='seat-add'),
    #获取排座
    path('seatSystem/getSeat/', v.SeatClass.getSeat, name='getSeat'),
    # 选中座位
    path('seatSystem/chooseSeat/',v.SeatClass.chooseSeat,name = 'chooseSeat'),

    #审核通过后回收座位
    path('seatSystem/systemBackSeat/',v.SeatClass.systemBackSeat,name = 'systemBackSeat'),

    path('seatSystem/addSeat/', v.SeatClass.addSeat, name='addSeat'),

    #取消座位上的员工

    path('seatSystem/noUserSeat/', v.SeatClass.noUserSeat, name='noUserSeat'),
    path('seatSystem/useSeatForm/',v.SeatClass.useSeatForm,name = 'useSeatForm'),
    path('seatSystem/useSeat/', v.SeatClass.useSeat, name='useSeat'),
    path('seatSystem/backSeat/', v.SeatClass.backSeat, name='backSeat'),
    path('seatSystem/delSeat/', v.SeatClass.delSeat, name='delSeat'),
    path('seatSystem/recycleSeat/', v.SeatClass.recycleSeat, name='recycleSeat'),
    path('seatSystem/getUserInfoBySeat/', v.SeatClass.getUserInfoBySeat, name='getUserInfoBySeat'),
    path('seatSystem/getUserSeatId/', v.SeatClass.getUserSeatId, name='getUserSeatId'),
    path('seatSystem/getUserIdSuggestion/', v.SeatClass.getUserIdSuggestion, name='getUserIdSuggestion'),
    path('seatSystem/test/',v.SeatClass.test,name = 'test'),
    path('seatSystem/zhipaiSeat/', v.SeatClass.zhipaiSeat, name='zhipaiSeat'),
    path('seatSystem/getSeatId/', v.SeatClass.getSeatId, name='getSeatId'),
    path('seatSystem/lotzhipaiSeat/', v.SeatClass.lotzhipaiSeat, name='lotzhipaiSeat'),
    path('seatSystem/lotChangeSeat/',v.SeatClass.lotChangeSeat,name = 'lotChangeSeat'),

    # 消息
    path('seatSystem/msgWindow/', v.message.msgWindow, name='msgWindow'),
    path('seatSystem/message-list/', v.message.messageList, name='messageList'),
    path('seatSystem/messageDetailForm/', v.message.messageDetailForm, name='messageDetailForm'),
    path('seatSystem/delMsg/', v.message.delMsg, name='delMsg'),
    path('seatSystem/messageDetail/', v.message.messageDetail, name='messageDetail'),
    path('seatSystem/changeReadStatus/', v.message.changeReadStatus, name='changeReadStatus'),

    #gonwei application
    path('seatSystem/seatApplicationAction/', v.SeatClass.seatApplicationAction, name='seatApplicationAction'),


    path('seatSystem/getUserDepartmentInfo/',v.UserClass.getUserDepartmentInfo,name = 'getUserDepartmentInfo'),

    path('seatSystem/getDepartmentSolutionInfo/', v.SeatClass.getDepartmentSolutionInfo, name='getDepartmentSolutionInfo'),

    #welcome页面部门雷达图
    path('seatSystem/getDepartmentSeatInfo/',v.DepartmentClass.getDepartmentSeatInfo,name = 'getDepartmentSeatInfo'),


    # 分組刪除

    path('seatSystem/delGroup/', v.Admin.delGroup, name='delGroup'),

    #
   # 部门
    path('seatSystem/depart/', v.UserClass.depart, name='depart'),

    path('seatSystem/delForm/', v.SeatClass.delForm, name='delForm'),

    #首页部门图
    path('seatSystem/getDepartSolutionInfo/', v.DepartmentClass.getDepartSolutionInfo, name='getDepartSolutionInfo'),

    # 搜索工位
    path('seatSystem/searchSeat/', v.SeatClass.searchSeat, name='searchSeat'),

#操作记录
    path('seatSystem/getRecord/', v.RecordClass.getRecord, name='getRecord'),
    path('seatSystem/operateRecord/', v.RecordClass.operateRecord, name='operateRecord'),

    path('seatSystem/seatInfo/', v.SeatClass.seatInfo, name='seatInfo'),
    path('seatSystem/getSeatInfo/', v.SeatClass.getSeatInfo, name='getSeatInfo'),

    path('seatSystem/emptySolution/', v.FloorClass.emptySolution, name='emptySolution'),
]
