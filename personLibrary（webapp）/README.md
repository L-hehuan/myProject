# 图书推荐app
---
## client
---
1. 总体来说是第一次开发的全栈应用，包括前端、服务端、数据库以及一系列构建功能，不过缺点也比较多，相关的详情不一一列出

2. 基于 uniapp 构建的webapp，使用 `colorui` 组件库对组件进行二次封装

3. 主要模块有个人中心模块、读书广场模块、图书中心模块、我的收藏模块

4. 向后台请求的数据使用 `uniapp` 封装好的 `uni.request` 进行数据请求与发送

5. 配置一系列登录用户才具有的功能，如阅读与收藏书籍功能、发布个人帖子、发布留言功能、验证和修改个人密码等

6. 注册模块需要提供手机号并输入正确的验证码，登录模块可选择手机号+验证码/密码登录

---
## server
---
1. 后端使用python开发，框架为 `Flask`，基本前端的功能都已实现，但功能上个人觉得还稍微不够完备，后期考虑使用其他框架重构前后端

2. 配置一系列前端请求的路由方式，对应的数据库增删改查操作

3. 封装 `mysql` 请求相应地API，调用阿里云短信模块，以支持前端相关的服务

4. 编写 `推荐算法`，根据用户的收藏习惯为用户推荐不同类别的书籍

5. 其余的可翻阅代码查看

---
# 个人博客（持续学习并更新中）
---
[甲子光年](https://jetmine.cn)