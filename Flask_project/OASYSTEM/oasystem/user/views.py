from oasystem.user.models import *
from flask import render_template, redirect, request, session
import os
from oasystem.user import userbp
from functools import wraps


# --------------------首页---------------------------
def login_check(func):
    @wraps(func)
    def inner():
        person_name = request.cookies.get('person_name')
        if person_name:
            return func()
        else:
            return redirect('/login/')

    return inner


import hashlib


def pwdjm(pwd):
    md5 = hashlib.md5(pwd.encode())
    result = md5.hexdigest()  # 生成密文
    return result


@userbp.route('/index/')
@userbp.route('/')
# @login_check
def index():
    news_list = News.query.all()
    attendance_list = Attendance.query.all()
    return render_template('index.html', news_list=news_list, attendance_list=attendance_list)


# ---------------职员管理--------------------------
# 职员列表
@userbp.route('/person_list/')
# @login_check
def person_list():
    person_obj_list = Person.query.all()
    return render_template('person.html', person_obj_list=person_obj_list)


# 添加职员
@userbp.route('/add_person/', methods=['GET', 'POST'])
# @login_check
def add_person():
    if request.method == 'GET':
        pos_list = Position.query.all()
        return render_template('add_person.html', pos_obj_list=pos_list)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        jobnum = request.form.get('jobnum')
        position_id = request.form.get('position_id')
        person_obj = Person()
        person_obj.name = username
        person_obj.password = pwdjm(password)
        person_obj.jobnum = jobnum
        person_obj.position_id = position_id
        person_obj.save()
        return redirect('/person_list/')


# 职员信息
@userbp.route('/person_detail/')
# @login_check
def person_detail():
    id = request.args.get('id')
    person_obj = Person.query.get(id)
    return render_template('profile.html', person_obj=person_obj)


# 修改职员信息
@userbp.route('/edit_person/', methods=['GET', 'POST'])
# @login_check
def edit_profile():
    if request.method == 'GET':
        id = request.args.get('id')
        person_obj = Person.query.get(id)
        position_list = Position.query.all()
        return render_template('edit_profile.html', person_obj=person_obj, position_obj_list=position_list)
    else:
        id = request.form.get('id')
        username = request.form.get('username')
        jobnum = request.form.get('jobnum')
        nikename = request.form.get('nickname')
        gender = request.form.get('gender')
        age = request.form.get('age')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        position_id = request.form.get('position_id')
        #  图片处理
        photo = request.files.get('photo')
        if photo.filename:
            # 查询数据库是否有图片,有则删除
            per_obj = Person.query.get(id)
            if per_obj.picture:
                os.remove(per_obj.picture)
            # 将新图片添加到path路径下,保存图片路径
            path = 'static/image/' + photo.filename
            photo.save(path)
        person_obj = Person.query.get(id)
        person_obj.name = username
        person_obj.jobnum = jobnum
        person_obj.nikename = nikename
        person_obj.gender = gender
        person_obj.age = age
        person_obj.phone = phone
        person_obj.email = email
        person_obj.address = address
        person_obj.position_id = position_id
        if photo.filename:
            person_obj.picture = path
        person_obj.update()
        return redirect('/person_list/')


# 删除职员
@userbp.route('/delete_person/')
def delete():
    id = request.args.get('id')
    person_obj = Person.query.get(id)
    path = person_obj.picture
    if path:
        os.remove(path)
    person_obj.delete()
    return redirect('/person_list/')


# 搜索职员
@userbp.route('/search_person/')
def search_person():
    name = request.args.get('name')
    person_obj_list = Person.query.filter(Person.name == name).all()
    return render_template('person.html', person_obj_list=person_obj_list)


# ------------------登陆------------------
@userbp.route('/login/', methods=['GET', 'POST'])
def login():
    error_msg = ''
    username = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        person_obj = Person.query.filter(Person.name == username, Person.password == pwdjm(password)).first()
        if person_obj:
            response = redirect('/')
            response.set_cookie('person_name', username)
            response.set_cookie('person_id', str(person_obj.id))
            session['person_name'] = username
            return response
        error_msg = ''
    return render_template('login.html', error_msg=error_msg, username=username)


# ------------------登出------------------
@userbp.route('/logout/')
def logout():
    response = redirect('/login/')
    response.delete_cookie('person_name')
    response.delete_cookie('person_id')
    session.get('person_name')
    session.clear()
    return response


# ---------------------部门管理---------------------
@userbp.route('/department_list/')
def department_list():
    dept_obj_list = Department.query.all()
    return render_template('department.html', dept_obj_list=dept_obj_list)


# 添加部门信息
@userbp.route('/add_dept/', methods=['GET', 'POST'])
def add_dept():
    if request.method == 'GET':
        return render_template('add_department.html')
    else:
        dept_name = request.form.get('name')
        dept_desc = request.form.get('description')
        dept_obj = Department(name=dept_name, desc=dept_desc)
        dept_obj.save()
        return redirect('/department_list/')


# 修改部门信息
@userbp.route('/edit_dept/', methods=['GET', 'POST'])
def edit_dept():
    if request.method == 'GET':
        id = request.args.get('id')
        dept_obj = Department.query.get(id)
        return render_template('edit_department.html', dept_obj=dept_obj)
    else:
        id = request.form.get('department_id')
        name = request.form.get('name')
        description = request.form.get('description')
        dept_obj = Department.query.get(id)
        dept_obj.name = name
        dept_obj.desc = description
        dept_obj.save()
        return redirect('/department_list/')


# 删除部门
@userbp.route('/delete_dept/')
def dept_delete():
    id = request.args.get('id')
    dept_obj = Department.query.get(id)
    pos_list = dept_obj.positions
    person_list = Person.query.all()
    for pos in pos_list:
        person_list = Person.query.filter(Person.position_id == pos.id)
    for person in person_list:
        if person.position.dept.name == dept_obj.name:
            person.delete()
    for pos in pos_list:
        pos.delete()
    dept_obj.delete()
    return redirect('/department_list/')


# 查看部门
@userbp.route('/position/')
def check_dept():
    id = request.args.get('id')
    dept_obj = Department.query.get(id)
    pos_list = dept_obj.positions
    return render_template('position.html', dept_obj=dept_obj, pos_list=pos_list)


# 添加职位
@userbp.route('/add_pos/', methods=['GET', 'POST'])
def add_pos():
    # if request.method == 'POST':
    dept_id = request.form.get('dept_id')
    name = request.form.get('name')
    level = request.form.get('level')
    pos_obj = Position()
    pos_obj.department_id = dept_id
    pos_obj.name = name
    pos_obj.level = level
    pos_obj.save()
    return redirect('/position/?id=' + str(dept_id))


# 编辑职位
@userbp.route('/edit_pos/', methods=['GET', 'POST'])
def edit_pos():
    id = request.form.get('pos_id')
    name = request.form.get('name')
    level = request.form.get('level')
    pos_obj = Position.query.get(id)
    pos_obj.name = name
    pos_obj.level = level
    pos_obj.update()
    return redirect('/position/?id=' + str(pos_obj.department_id))


# 删除职位
@userbp.route('/delete_pos/')
def delete_pos():
    pos_id = request.args.get('id')
    pos_obj = Position.query.get(pos_id)
    pos_obj.delete()
    return redirect('/position/?id=' + str(pos_obj.department_id))


# -------------------考勤-------------------
import datetime


@userbp.route('/att_me/', methods=['GET', 'POST'])
def attendance_me():
    reason = request.form.get('reason')
    type = request.form.get('type')
    day = request.form.get('day')
    start = request.form.get('start')
    end = request.form.get('end')
    attendance_me_obj = Attendance()
    attendance_me_obj.reason = reason
    attendance_me_obj.atype = type
    attendance_me_obj.adate = day
    attendance_me_obj.start_time = datetime.datetime.strptime(start, '%Y-%m-%d')
    attendance_me_obj.end_time = datetime.datetime.strptime(end, '%Y-%m-%d')
    person_id = request.cookies.get('person_id')
    attendance_me_obj.person_id = person_id
    attendance_me_obj.save()
    return redirect('/att_list_me/')


@userbp.route('/att_list_me/')
def att_list_me():
    person_id = request.cookies.get('person_id')
    att_obj_list = Attendance.query.filter(Attendance.person_id == person_id).all()
    return render_template('attendance_me.html', att_obj_list=att_obj_list)


# 下属考勤
@userbp.route('/att_list_sub/', methods=['GET', 'POST'])
def att_sub():
    person_id = request.cookies.get('person_id')
    person_obj = Person.query.get(person_id)
    pos_obj = person_obj.position
    print(pos_obj)
    level = pos_obj.level
    dept_id = pos_obj.department_id
    pos_obj_list = Position.query.filter(Position.level < level, Position.department_id == dept_id).all()
    person_list = []
    for pos_obj in pos_obj_list:
        person_list += pos_obj.persons
    att_list = []
    for person_obj in person_list:
        att_obj_list = person_obj.attendances
        att_list += att_obj_list
    return render_template('attendance_subordinate.html', att_list=att_list)


@userbp.route('/update_att_sub/')
def update_att_sub():
    id = request.args.get('id')
    status = request.args.get('status')
    att_obj = Attendance.query.get(id)
    att_obj.astauts = status
    person_name = request.cookies.get('person_name')
    att_obj.examine = person_name
    att_obj.update()
    return redirect('/att_list_sub/')


# ---------------新闻管理------------------
# @userbp.route('/show_news/')
# def show_news():
#     return

@userbp.route('/news_list/')
def news_list():
    news_list = News.query.all()
    return render_template('news.html', news_list=news_list)


@userbp.route('/add_new/', methods=['GET', 'POST'])
def add_new():
    if request.method == 'GET':
        return render_template('add_news.html')
    else:
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        picture = request.files.get('picture')
        new_obj = News()
        new_obj.title = title
        new_obj.author = author
        new_obj.content = content
        new_obj.ntime = datetime.datetime.now()
        # path = '../static/image/' + picture.filename
        # picture.save(path)
        new_obj.save()
        return redirect('/news_list/')


@userbp.route('/detail_new/')
def detail_new():
    id = request.args.get('id')
    new_obj = News.query.get(id)
    return render_template('detail_new.html', new_obj=new_obj)


@userbp.route('/edit_new/', methods=['GET', 'POST'])
def edit_new():
    if request.method == 'GET':
        id = request.args.get('id')
        new_obj = News.query.get(id)
        return render_template('edit_news.html', new_obj=new_obj)
    else:
        id = request.args.get('id')
        new_obj = News.query.get(id)
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        print(content)
        new_obj.title = title
        new_obj.ntime = datetime.datetime.now()
        new_obj.author = author
        new_obj.content = content
        new_obj.update()
        return redirect('/news_list/')


@userbp.route('/delete_new/')
def delete_new():
    id = request.args.get('id')
    new_obj = News.query.get(id)
    new_obj.delete()
    return redirect('/news_list/')


@userbp.route('/per_list/')
def per_list():
    per_list = Permission.query.all()
    return render_template('permission.html', per_list=per_list)


@userbp.route('/add_permission/', methods=['GET', 'POST'])
def add_permission():
    if request.method == 'GET':
        return render_template('add_permission.html')
    else:
        name = request.form.get('name')
        desc = request.form.get('desc')
        per_obj = Permission()
        per_obj.name = name
        per_obj.desc = desc
        per_obj.save()
        return redirect('/per_list/')


@userbp.route('/delete_per/')
def delete_per():
    id = request.args.get('id')
    per_obj = Permission.query.get(id)
    per_obj.delete()
    return redirect('/per_list/')


@userbp.route('/edit_permission/', methods=['GET', 'POST'])
def edit_permission():
    if request.method == 'GET':
        id = request.args.get('id')
        per_obj = Permission.query.get(id)
        return render_template('edit_permission.html', per_obj=per_obj)
    else:
        id = request.args.get('id')
        per_obj = Permission.query.get(id)
        name = request.form.get('name')
        desc = request.form.get('desc')
        per_obj.name = name
        per_obj.desc = desc
        per_obj.update()
        return redirect('/per_list/')


@userbp.route('/position_permission/', methods=['GET', 'POST'])
def position_permission():
    if request.method == 'GET':
        id = request.args.get('id')
        per_obj = Permission.query.get(id)
        pos_objs = per_obj.positions
        pos_id_list = []
        for pos_obj in pos_objs:
            pos_id_list.append(pos_obj.id)
        pos_obj_list = Position.query.all()
        return render_template('position_permission.html', pos_obj_list=pos_obj_list, id=id, pos_id_list=pos_id_list)
    else:
        id = request.args.get('id')
        position_ids = request.form.getlist('position_ids')
        pos_list = []
        for position_id in position_ids:
            pos_obj = Position.query.get(position_id)
            pos_list.append(pos_obj)
        per_obj = Permission.query.get(id)
        per_obj.positions = pos_list
        per_obj.save()
        return redirect('/per_list/')


# @userbp.add_app_template_global
# def show_hidden():
#     result = {
#         'new': False,
#         'persons': False,
#         'work': False,
#         'per': False
#     }
#     person_obj_id = request.cookies.get('person_id')
#     person_obj = Person.query.get(person_obj_id)
#     pos_obj = person_obj.position
#     per_obj_list = pos_obj.permissions
#     for per_obj in per_obj_list:
#         if per_obj.name == '新闻管理':
#             result['new'] = True
#         if per_obj.name == '人事管理':
#             result['persons'] = True
#         if per_obj.name == '考勤管理':
#             result['work'] = True
#         if per_obj.name == '权限管理':
#             result['per'] = True
#     return result

# ---------------- 分页 ---------------------
