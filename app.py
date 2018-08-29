# -*- coding: utf-8 -*-

import os
import json
import time

from models import Database
from models import global_var
from flask import Flask, render_template, redirect, url_for, request, send_from_directory, flash
from werkzeug import secure_filename

from models.forms import LoginForm
from flask_wtf.csrf import CSRFProtect
from models.User import User
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
# app.config['ENCODING'] = 'gbk'
app.config['ENCODING'] = 'utf-8'
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/uploads'
app.config['ABAQUS_INPUT_FOLDER'] = os.getcwd() + '/static/abaqus_input/'
app.config['IMG_FOLDER'] = os.getcwd() + '/static/img/'
app.config['FURNITURE_FOLDER'] = os.getcwd() + '/static/uploads/furniture'
app.config['FURNITURE_THUMBNAIL_FOLDER'] = os.getcwd() + '/static/uploads/furniture_thumbnail'
app.config['TEMPLATE_FOLDER'] = os.getcwd() + '/static/uploads/template'
app.config['TEMPLATE_THUMBNAIL_FOLDER'] = os.getcwd() + '/static/uploads/template_thumbnail'

global_var.progress_percent = 0

app.secret_key = os.urandom(24)
# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)

# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)

@app.route('/show_progress')
def show_progress():
    return str(global_var.progress_percent)

ALLOWED_EXTENSIONS = set(['xlsx','jpg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/certification_file/<filename>')
def certification_file(filename):
    return send_from_directory(app.config['IMG_FOLDER'],
                               filename)

@app.route('/certification', methods=['GET', 'POST'])
def certification():
    if request.method == 'POST':
        import pandas as pd
        from models.certification import certification
        file = request.files['excelfile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            df = pd.read_excel(app.config['UPLOAD_FOLDER'] + '/' + filename)           
            data = df.to_dict(orient='records')
            for d in data:
                certification_name = certification( img_folder=app.config['IMG_FOLDER'],
                                                    number=d[u'编号'],
                                                    qrcode_text=d[u'二维码信息'],
                                                    name=d[u'产品名称'],
                                                    furniture_filename=app.config['FURNITURE_FOLDER'] + '/' + d[u'家具图片'],
                                                    template_filename=app.config['TEMPLATE_FOLDER'] + '/' + d[u'模板图片'] )
                d['url'] = url_for('certification_file', filename=certification_name)
            return render_template('certification.html', file_url=file_url, data=data)

    return render_template('certification.html', file_url='#', data=[])

@app.route('/furniture', methods=['GET', 'POST'])
def furniture():
    from models.thumbnail import thumbnail
    from models.furniture import get_FileModifyTime

    def data(filename_list):
        data_list = []
        for filename in filename_list:
            url = '/static/uploads/furniture' + '/' + filename
            url_thumb = '/static/uploads/furniture_thumbnail' + '/' + filename
            data_list.append({  'file':unicode(filename,app.config['ENCODING']),
                                'url':unicode(url,app.config['ENCODING']),
                                'url_thumb':unicode(url_thumb,app.config['ENCODING']),
                                'modify_time':get_FileModifyTime(os.path.join(app.config['FURNITURE_FOLDER'],filename))
                            })
        return data_list

    files_list = os.listdir(app.config['FURNITURE_FOLDER'])
    data_list = data(files_list)

    if request.method == 'POST':
        for file in request.files.getlist('photo'):
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['FURNITURE_FOLDER'], filename))
                thumbnail(filename,app.config['FURNITURE_FOLDER'],app.config['FURNITURE_THUMBNAIL_FOLDER'])
        files_list = os.listdir(app.config['FURNITURE_FOLDER'])
        data_list = data(files_list)

    return render_template('furniture.html', data_list=data_list)

@app.route('/template', methods=['GET', 'POST'])
def template():
    from models.thumbnail import thumbnail
    from models.furniture import get_FileModifyTime

    def data(filename_list):
        data_list = []
        for filename in filename_list:
            url = '/static/uploads/template' + '/' + filename
            url_thumb = '/static/uploads/template_thumbnail' + '/' + filename
            data_list.append({  'file':unicode(filename,app.config['ENCODING']),
                                'url':unicode(url,app.config['ENCODING']),
                                'url_thumb':unicode(url_thumb,app.config['ENCODING']),
                                'modify_time':get_FileModifyTime(os.path.join(app.config['TEMPLATE_FOLDER'],filename))
                            })
        return data_list

    files_list = os.listdir(app.config['TEMPLATE_FOLDER'])
    data_list = data(files_list)

    if request.method == 'POST':
        for file in request.files.getlist('photo'):
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['TEMPLATE_FOLDER'], filename))
                thumbnail(filename,app.config['TEMPLATE_FOLDER'],app.config['TEMPLATE_THUMBNAIL_FOLDER'])
        files_list = os.listdir(app.config['TEMPLATE_FOLDER'])
        data_list = data(files_list)

    return render_template('template.html', data_list=data_list)

@app.route('/furniture/delete/<filename>')
def furniture_delete_file(filename):
    original_fullname = os.path.join(app.config['FURNITURE_FOLDER'],filename)
    os.remove(original_fullname)
    thumbnail_fullname = os.path.join(app.config['FURNITURE_THUMBNAIL_FOLDER'],filename)
    os.remove(thumbnail_fullname)
    return redirect(url_for('furniture'))

@app.route('/template/delete/<filename>')
def template_delete_file(filename):
    original_fullname = os.path.join(app.config['TEMPLATE_FOLDER'],filename)
    os.remove(original_fullname)
    thumbnail_fullname = os.path.join(app.config['TEMPLATE_THUMBNAIL_FOLDER'],filename)
    os.remove(thumbnail_fullname)
    return redirect(url_for('template'))

@app.route('/static/abaqus_input/<filename>')
def abaqus_input(filename):
    return send_from_directory(app.config['ABAQUS_INPUT_FOLDER'], filename)

@app.route('/thread', methods=['GET', 'POST'])
@login_required
def thread():
    from models.thread_external_MJ import thread_external_MJ
    if request.method == 'POST':
        d = float(request.form["d"])
        P = float(request.form["P"])
        L = float(request.form["L"])
        n = int(request.form["n"])
        m = int(request.form["m"])
        seg = int(request.form["seg"])
        bound = int(request.form["bound"])
        filename, is_done = thread_external_MJ(app.config['ABAQUS_INPUT_FOLDER'], d=d, P=P, L=L, n=n, m=m, seg=seg, bound=bound)
        if is_done:
            return render_template('thread.html', progress_done = "true", filename = filename)
    return render_template('thread.html', progress_done = "false")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User(user_name)
        if user.verify_password(password):
            login_user(user, remember=remember_me)
            return redirect(url_for('index'))
            # return redirect(request.args.get('next') or url_for('index'))
        else:
            flash(u'用户名或密码错误', 'message')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    # db = Database()
    # db.execute(
    #     ''' 
    #     create table if not exists student(
    #         id      text primary key,
    #         name    text not null,
    #         birth   text 
    #     )
    #     ''' 
    # )
    # for i in range(0,10):
    #     db.execute("insert into student values('id1" + str(i) + "', 'name1" + str(i) + "', 'birth1" + str(i) + "')")
    # db.execute("insert into student values('id01', 'name01', 'birth01')")
    # db.execute("insert into student values('id02', 'name02', 'birth01')")
    # db.execute("insert into student values('id03', 'name03', 'birth01')")

    # print(db.getColumnNames("select * from student"))
    # print(db.getCount("select * from student"  ))
    # print(db.getString("select name from student where id = ? ", "id01"  ))
    # print(db.getString("select name from student where birth = ? ", "birth01"  ))

    # s = db.executeQuery("select * from student where name = ? or 1=1", "name01")
    
    # db.close()

    if request.method == 'POST':
        progress_done, filename = process_data()
        if progress_done:
            return render_template('index.html', progress_done = "true", filename = filename)
    #     db = Database()
    #     count = db.getCount("select * from student")
    #     sql = "insert into student values('%s', '%s', '%s')" % (count,request.form["name"],request.form["birth"])
    #     # sql = "insert into student values('%s', '%s', '%s')" % (count,count,count)
    #     db.execute(sql)
    #     s = db.executeQuery("select * from student where name = ? or 1=1", "name01")
    #     db.close()
    #     return render_template('index.html', data=s)

    return render_template('index.html', progress_done = "false")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)