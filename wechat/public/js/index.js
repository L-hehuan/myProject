var socket = io('http://192.168.31.239:7878');
var login_img = document.querySelector('.login_img');
var login_but = document.querySelector('#login_but');
var usernn = document.querySelector('.login_name').getElementsByTagName('input')[0];
var home_chat =document.getElementsByClassName('home-chat')[0]
var home = document.querySelector('#home');
var login = document.querySelector('#login');
var user_img = home.getElementsByClassName('userimg')[0];
var user_name = home.getElementsByClassName('username')[0];
var home_left_bottom = home.getElementsByClassName('home-left-bottom')[0];
var count = document.getElementById('usercount')
var sendm = document.getElementById('sendmessage')
var chat_text = document.getElementById('chat_text')
var uname;
var uavatar;
var sendfile = document.getElementById('fileselect')
var photo = document.getElementById('sendphoto')
var imgms = {

}
// console.log(login_img.getElementsByClassName('sel')[0].getAttribute('src'))
login_img.addEventListener('click',function(e){
    var e = e || window.event;
    var target = e.target || e.which || e.srcElement;
    if(target.nodeName == 'IMG'){
        for(var i=0;i<=login_img.children.length-1;i++){
            login_img.children[i].className=''
        }
        target.className = 'sel';
    }
})
login_but.onclick = function(){
    var value = usernn.value;
    var avatar = login_img.getElementsByClassName('sel')[0].getAttribute('src')
    if(value.length==0 || value=='' || /(^(\s)|(\s)$)/g.test(value)){
        alert('请输入一个正确的用户名');
        return;
    }
    socket.emit('login',{
        username:value,
        avatar:avatar,
    })
}

socket.on('loginerror',data => {
    alert('用户名已存在,请重新输入')
})
socket.on('loginSuccess', data =>{
    login.style.display='none';
    home.style.display='flex';
    user_img.setAttribute('src',login_img.getElementsByClassName('sel')[0].getAttribute('src'));
    user_name.innerText = usernn.value;
    uname=data.username
    uavatar=data.avatar
})

socket.on('adduser',data => {
    var newdiv = document.createElement('div');
    newdiv.className='addtips';
    newdiv.innerHTML=`<span style="color:gray;">${new Date().toLocaleTimeString()}</span><span style="color:black;margin-top:4px;">用户<span style="margin:0 3px;color:green;">${data.username}</span>加入了群聊</span>`
    home_chat.appendChild(newdiv)
    home_chat.children[home_chat.children.length-1].scrollIntoView(false)
})

socket.on('userList',data => {
    home_left_bottom.innerHTML=''
    data.forEach(item => {
        var user_list = document.createElement('div');
        var useimg = document.createElement('img');
        var un = document.createElement('span');
        user_list.className='home-left-con'
        useimg.className='userimg'
        un.className='username'
        useimg.setAttribute('src',item.avatar)
        un.innerText=item.username
        user_list.appendChild(useimg);
        user_list.appendChild(un)
        home_left_bottom.appendChild(user_list);
    });
    count.innerText=`(${data.length})`
})

socket.on('deluser',data => {
    var newdiv = document.createElement('div');
    newdiv.className='addtips';
    newdiv.innerHTML=`<span style="color:gray;">${new Date().toLocaleTimeString()}</span><span style="color:red;margin-top:4px;">用户<span style="margin:0 3px;color:green;">${data.username}</span>离开了群聊</span>`
    home_chat.appendChild(newdiv)
    home_chat.children[home_chat.children.length-1].scrollIntoView(false)
})

sendm.onclick = function(){
   home_chat.scrollIntoView()
   var text =  chat_text.value.trim();
   if(!text){
       alert('无内容可发送');
       return
   }else{
       socket.emit('sendMessage',{
           msg:text,
           username:uname,
           avatar:uavatar
       })
   }
   chat_text.value=''
}

socket.on('recieve',data=>{
    if(data.username===uname){
        var mymessage = document.createElement('div');
        mymessage.className='mymessage';
        var my_img = document.createElement('img');
        var my_span = document.createElement('span');
        var me_span = document.createElement('span')
        my_img.setAttribute('src',data.avatar);
        my_span.innerText=data.username
        me_span.innerText=data.msg
        mymessage.appendChild(me_span);
        mymessage.appendChild(my_span);
        mymessage.appendChild(my_img);
        home_chat.appendChild(mymessage)
    }else{
        var othmessage = document.createElement('div');
        othmessage.className='othermessage';
        var oh_img = document.createElement('img');
        var oh_span = document.createElement('span');
        var oh2_span = document.createElement('span')
        oh_img.setAttribute('src',data.avatar);
        oh_span.innerText=data.username
        oh_span.style.cssText='margin-right: 10px;align-self: start; color: white;height: 40px;font-size: 12px;'
        oh2_span.style.cssText='font-size: 14px;height: 40px; white-space: pre-wrap;color:black;line-height:40px;background-color: greenyellow;padding: 3px;'
        oh2_span.innerText=data.msg
        othmessage.appendChild(oh_img);
        othmessage.appendChild(oh_span);
        othmessage.appendChild(oh2_span);
        home_chat.appendChild(othmessage);
    }
    home_chat.children[home_chat.children.length-1].scrollIntoView(false)
})

sendfile.onchange =function(e){
    var simg = this.files[0];
    var fr = new FileReader()
    fr.readAsDataURL(simg)
    fr.onload = function(){
        socket.emit('sendimg',{
            username:uname,
            avatar:uavatar,
            img:fr.result
        })
    }
}

socket.on('allimg',data => {
        if(data.username!=uname){
            var othmessage = document.createElement('div');
            othmessage.className='othermessage';
            var oh_img = document.createElement('img');
            var oh_span = document.createElement('span');
            var allimg = document.createElement('img')
            oh_img.setAttribute('src',data.avatar);
            oh_span.innerText=data.username;
            oh_span.style.cssText='margin-right: 10px;align-self: start; color: white;height: 40px;font-size: 12px;'
            allimg.setAttribute('src',data.img)
            othmessage.appendChild(oh_img);
            othmessage.appendChild(oh_span);
            othmessage.appendChild(allimg);
            home_chat.appendChild(othmessage);
        }else{
            var mymessage = document.createElement('div');
            mymessage.className='mymessage';
            var my_img = document.createElement('img');
            var my_span = document.createElement('span');
            var myimg = document.createElement('img')
            my_img.setAttribute('src',data.avatar);
            my_span.innerText=data.username;
            myimg.setAttribute('src',data.img)
            mymessage.appendChild(myimg)
            mymessage.appendChild(my_span);
            mymessage.appendChild(my_img);
            home_chat.appendChild(mymessage)
        }
        home_chat.children[home_chat.children.length-1].scrollIntoView(false)
})