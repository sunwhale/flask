# flask

图片生成过程中需要字体文件“simsun.ttc”，下载地址 https://github.com/sonatype/maven-guide-zh/raw/master/content-zh/src/main/resources/fonts/simsun.ttc

# 服务器版本 CentOS 7.4

# 安装 Nginx Web 服务器

yum install nginx

systemctl start nginx

# 安装 uWSGI

yum install python-devel

pip install uwsgi

# 安装 git

yum install git

# 下载网站源文件

git clone https://github.com/sunwhale/flask.git

# 在这里我们可以使用虚拟环境VirtualEnv，官方文档 https://virtualenv.readthedocs.org/en/latest/

pip install virtualenv

# 进入网站根目录，配置虚拟环境

cd flask

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

deactivate

# 编辑默认的 Nginx 配置文件

vim /etc/nginx/nginx.conf

```
    server {
        listen       80 default_server;
        server_name  47.93.195.1;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
        include      uwsgi_params;
        uwsgi_pass   127.0.0.1:5000;  # 指向 uwsgi 所应用的内部地址,所有请求将转发给 uwsgi 处理
        uwsgi_param  UWSGI_PYHOME /root/flask/venv; # 指向虚拟环境目录
        uwsgi_param  UWSGI_CHDIR  /root/flask; # 指向网站根目录
        uwsgi_param  UWSGI_SCRIPT app:app; # 指定启动程序
        }
```

找到 http{} 字段并添加以下内容

```
    client_max_body_size 20m; # 20M为允许的文件大小
```

# 建立配置文件 uwsgi.ini

vim uwsgi.ini

```
[uwsgi]

# uwsgi 启动时所使用的地址与端口
socket = 127.0.0.1:5000

# 指向网站目录
chdir = /root/flask/

# python 启动程序文件
wsgi-file = app.py

# python 程序内用以启动的 application 变量名
callable = app

# 处理器数
processes = 1

# 线程数
threads = 2

# 状态检测地址
stats = 127.0.0.1:9191

# 使进程在后台运行，并将日志打到指定的日志文件。
daemonize = /root/flask/uwsgi_httpServer.log

# 不记录请求信息的日志。只记录错误以及uWSGI内部消息到日志中。
disable-logging = true
```

# 启动、停止和升级 uwsgi

```
uwsgi --ini uwsgi.ini

uwsgi uwsgi.ini --deamonize # 后台运行启动
 
uwsgi --stop uwsgi.pid  # 停止服务
 
uwsgi --reload uwsgi.pid  # 可以无缝重启服务
```

# 安装 supervisor 监测 uwsgi 运行状态

yum install supervisor

vim supervisord.conf

```
[program:flask] # 项目名称
command = uwsgi --ini /root/flask/uwsgi.ini # 跟手动启动的命令一样
directory = /root/flask # 命令程序所在目录
user = root
stopsignal = QUIT
autostart = true
autorestart = true
stdout_logfile = /root/flask/supervisor_flask.log # 运行日志
stderr_logfile = /root/flask/supervisor_flask_err.log # 错误日志
```

