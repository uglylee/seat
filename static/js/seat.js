



        function sendMessageToAdmin(obj,x,y){

            $.ajax({
            url: "{% url 'sendMessageToAdmin' %}",
            type: "post",
            contentType: 'application/json',
            dataType: "json",
            data: JSON.stringify({'user_id': '000001', 'seat_id': 'A022', 'send_msg': '申请工位'}),
            success: function (data) {
            layer.msg('发送成功', {icon: 6});
            },
            error: function (data) {
            layer.msg('新增失败', {icon: 5});
            return false;
            }
            }
            )

        }

        function seatNoOne(obj){

      var positionXY;
    positionXY=getMousePosition(obj);
            positionY=positionXY[0];
            positionX=positionXY[1];
            layer.msg('未分配',{offset:[positionX,positionY]})
        }

        function seatWaiting(obj,event,x,y,id){
            positionXY=getMousePosition(obj);
            positionY=positionXY[0];
            positionX=positionXY[1];
            layer.msg('审核中,申请部门XXX',{offset:[positionX,positionY]})

        }
        function seatWaitForUser(obj,event,x,y,id){
            positionXY=getMousePosition(obj);
            positionY=positionXY[0];
            positionX=positionXY[1];
            layer.msg('属于XXX部门，未使用',{offset:[positionX,positionY]})

        }



        function delUserAction(obj){

            console.log('dianji珊瑚了')
        }

        function getMousePosition(obj,event){
            var positionX,positionY,top;
          {##获取滚动条高度#}
           top = document.documentElement.scrollTop;
            var e =event || window.event;
            positionY= (e.clientX+document.body.scrollLeft+document.documentElement.scrollLeft)+'px';
            positionX = (e.clientY+document.body.scrollTop+document.documentElement.scrollTop-top)+'px';
            return [positionY,positionX]
        }

        function RightWhiteAction(obj,e,x,y){
                console.log('右键点击了');
            positionXY=getMousePosition(obj,e);
            positionY=positionXY[0];
            positionX=positionXY[1];
            {#window.oncontextmenu=function(e){#}
//取消默认的浏览器自带右键 很重要！！
                e.preventDefault();
                //获取我们自定义的右键菜单
            console.log('右键点击了');
                    layer.msg('哈哈',{offset:[positionX,positionY]})
                //关闭右键菜单，很简单
        }

        function closeMsg(){
            var index = layer.msg()
             layer.close(index)
        }
        function showNoUsedSeatInfo(obj,event,x,y){
             var positionX,positionY,top;
           top = document.documentElement.scrollTop;
            var e =event || window.event;
            positionY= (e.clientX+document.body.scrollLeft+document.documentElement.scrollLeft+60)+'px';
            positionX = (e.clientY+document.body.scrollTop+document.documentElement.scrollTop-top)+'px';
              $.ajax({
        url:"{% url 'getUserInfoBySeat' %}",
        type:"post",
        contentType: 'application/json',
        dataType:"json",
         data:JSON.stringify({'x':x,'y':y,'floor':floor,'title':'noUsed'}),
        success:function (data) {

        var info = data.info;
                        let information ;
                            information = "状态:"+info[0]['status']+"  <br>部门:"+info[0]['department_id__name']+"  <br>座位:"+info[0]['seat_id']+""
                layer.msg(information,{offset:[positionX,positionY]});
            }})
        }
        function showUsedSeatInfo(obj,event,x,y) {
            var positionX, positionY, top;
            top = document.documentElement.scrollTop;
            var e = event || window.event;
            positionY = (e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft + 60) + 'px';
            positionX = (e.clientY + document.body.scrollTop + document.documentElement.scrollTop - top) + 'px';
            $.ajax({
                url: "{% url 'getUserInfoBySeat' %}",
                type: "post",
                contentType: 'application/json',
                dataType: "json",
                data: JSON.stringify({'x': x, 'y': y, 'floor': floor, 'title': 'used'}),
                success: function (data) {

                    var info = data.info;
                    let information;
                    information = "状态:" + info[0]['status'] + "  <br>用户编号:" + info[0]['user_id'] + " <br> 姓名:" + info[0]['name'] + " <br>部门:" + info[0]['department_id__name'] + "  <br>座位:" + info[0]['seat_id'] + ""
                    layer.msg(information, {offset: [positionX, positionY]});
                }
            })

