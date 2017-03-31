# 功能
通过局域网实现文字在可联网设备中的传输
- **上传数据：**
设备接入局域网，访问数据中转网页， 在网页中输入文本，并提交输入

- **接收数据：**
设备接入局域网，访问数据中转网页，在网页中的文本显示区可以复制文本到设备的剪贴板中

# 详细步骤
- [简书_ubuntu中的web服务器配置](http://www.jianshu.com/p/0988624ff307)

# 安装
通过 apt-get 安装: python3-dev, nginx, virtualenv
创建并进入虚拟环境：
```c
virtualenv webserver
cd webserver
source bin/activate
```
使用 pip 安装: uwsgi, django

# 配置
- 修改 nginx.conf 文件
将 alias 后面的路径修改为自己电脑中的路径，例如：
media下的：/home/zooo/word-share-web/mysite/media;
修改为：/home/geekz/webserver/word-share-web/mysite/media;
之后的 static, /, 也做相同修改
- 将 nginx.conf 链接到 nginx 目录中
`sudo ln -s ~/webserver/word-share-web/mysite/nginx.conf /etc/nginx/sites-enabled`
- 修改 uwsgi.ini 文件
用样修改对应的路径

# 启动服务及测试
- **启动 nginx：** `sudo /etc/init.d/nginx start`
- **启动 uwsgi：** `uwsgi --ini uwsgi.ini`
- **测试：** 在浏览器中输入 `127.0.0.1:801`进入文字分享网页

# 让同一个局域网中的电脑能够访问
- 得到本机 ip
- 将 ip 添加到 mysite/setting.py 的 ALLOWED_HOSTS 中

# BUGS
- BUGs 1: 在起 uwsgi 的时候提示
`!!! no internal routing support, rebuild with pcre support !!!`
**解决方法：**
```c
sudo apt-get install libpcre3 libpcre3-dev
pip install uwsgi -I --no-cache-dir
```

- Bugs 2: 在网页中输入 `127.0.0.1:8000` 的时候出现：
`invalid request block size: 21573 (max 4096)...skip`
原因：在 uwsgi 的配置中设置的为 socket 通信，而web端发送的数据格式是基于 http 协议的因此直接向 uwsgi 监控的端口提交数据就会被忽略。
解决方法: 将 uwsgi 设置为直接支持 http = 127.0.0.1:8000
或者输入 `127.0.0.1:801` --向 nginx 提交 web 的数据


