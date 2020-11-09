var app = require('express')()
var server = require('http').Server(app)
var io = require('socket.io')(server)
app.all("*",function(req,res,next){
    res.header("Access-Control-Allow-Origin","*");// 允许所有跨域请求
    res.header("Access-Control-Allow-Headers","xCors");//允许请求头中携带xCors
    res.header("Access-Control-Allow-Methods","GET,POST,DELETE,PUT,OPTIONS,HEAD,FETCH");
    // 
    res.header("Access-control-max-age", 1000); // 设置Access-Control-Max-Age超时时间
    next();
// express中间件
})
const users = []
server.listen(7878,() =>{
    console.log('服务器启动成功')
})
// 将public资源目录设为访问主页
app.use(require('express').static('public'))

app.get('/',function(req,res){
    res.redirect('/html/index.html')
})

io.on('connection',function(socket){
    socket.on('login',data =>{
        let user =users.find(item => item.username === data.username);
        if(user){
            // alert('用户名已被使用,请重新输入')
            socket.emit('loginerror',{msg:'登陆失败'});
            console.log('登陆失败')
        }else{
            users.push(data);
            socket.emit('loginSuccess',data);
            io.emit('adduser',data);
            //socket.emit:告诉当前用户
            //io.emit:广播事件

            io.emit('userList',users)
            socket.username=data.username
            socket.avater =data.avater
        }
    })
    socket.on('disconnect',()=>{
        let idx = users.findIndex(item =>item.username === socket.username);
        users.splice(idx,1);
        io.emit('deluser',{
            username:socket.username,
            avater:socket.avater
        })
        io.emit("userList",users)
    })
    socket.on('sendimg',data => {
        io.emit('allimg',data)
    })
    socket.on('sendMessage',data => {
        io.emit('recieve', data)
    })
})