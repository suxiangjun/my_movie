#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "junesu"
# Date: 2018-07-05
from . import home
from flask import render_template,redirect,url_for,flash,session,request
from app.home.forms import RegistForm,LoginForm,UserForm
from app.models import User,db,Userlog
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid
import os
from app import app
import datetime
# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename

@home.route("/")
def index():
    return render_template("home/index.html")

@home.route("/login/",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if not user.check_pwd(data["pwd"]):
            return redirect(url_for('home.login'))
        session["user"] = data["name"]
        session['user_id'] = user.id
        userlog=Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html",form=form)

@home.route("/logout/",methods=["GET"])
def logout():
    session.pop("user",None)
    session.pop("user_id",None)
    return  redirect(url_for("home.login"))

@home.route("/regist/",methods=["GET","POST"])
def regist():
    form=RegistForm()
    if form.validate_on_submit():
        data=form.data
        user=User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功","ok")
    return render_template("home/regist.html",form=form)

@home.route("/user/",methods=["GET","POST"])
def user():
    form=UserForm()
    user=User.query.filter_by(id=session['user_id']).first()
    if request.method=="GET":
        form.name.data=user.name
        form.email.data=user.email
        form.phone.data=user.phone
        form.info.data=user.info
    if form.validate_on_submit():
        data=form.data
        file_face = secure_filename(form.face.data.filename)  # 安全性
        if not os.path.exists(app.config["FACE_DIR"]):
            os.makedirs(app.config["FACE_DIR"])
            os.chmod(app.config["FACE_DIR"], "rw")  # 目录权限
        face = change_filename(file_face)
        form.face.data.save(app.config["FACE_DIR"] + face)
        user.name=data["name"]
        user.email=data["email"]
        user.phone=data["phone"]
        user.info=data["info"]
        user.face=face
        db.session.add(user)
        db.session.commit()
        flash("编辑成功","ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html",form=form,user=user)
#修改密码
@home.route("/pwd/")
def pwd():
    return render_template("home/pwd.html")

@home.route("/comments/")
def comments():
    return render_template("home/comments.html")

@home.route("/loginlog/")
def loginlog():
    return render_template("home/loginlog.html")

@home.route("/moviecol/")
def moviecol():
    return render_template("home/moviecol.html")

@home.route("/animation/")
def animation():
    return render_template("home/animation.html")

@home.route("/search/")
def search():
    return render_template("home/search.html")

@home.route("/play/")
def play():
    return render_template("home/play.html")

