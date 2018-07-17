#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "junesu"
# Date: 2018-07-05
from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm, MovieForm,PreviewForm
from app.models import Admin, Tag, db, Movie,Preview
from functools import wraps  # 装饰器
from app import app
import os, uuid, datetime
from werkzeug.utils import secure_filename  # filename 转化为安全的


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))  # 获取到要跳转到的地址
        return f(*args, **kwargs)

    return decorated_function


@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


@admin.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误!")
            return redirect(url_for('admin.login'))
        session["admin"] = data["account"]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout/")
@admin_login_req
def logout():
    print(session["admin"])
    session.pop("admin", None)
    print(session["admin"])
    return redirect(url_for("admin.login"))


@admin.route("/pwd/")
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


# 编辑标签
@admin.route("/tag/add/", methods=["GET", "POST"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash("名称已经存在！", "err")
            return redirect(url_for("admin.tag_add"))
        tag = Tag(
            name=data["name"]

        )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功！", "ok")
        return redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 标签列表
@admin.route("/tag/list/<int:page>/", methods=["GET"])
@admin_login_req
def tag_list(page):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime
    ).paginate(page=page, per_page=5)  # 传入分页
    return render_template("admin/tag_list.html", page_data=page_data)


# 标签删除
@admin.route("/tag/del/<int:id>/", methods=["GET"])
@admin_login_req
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()  # 查询不到返回404
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签成功！", "ok")
    return redirect(url_for("admin.tag_list", page=1))


# 编辑标签
@admin.route("/tag/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag_count == 1 and tag.name != data["name"]:
            flash("名称已经存在！", "err")
            return redirect(url_for("admin.tag_edit", id=id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功！", "ok")
        return redirect(url_for("admin.tag_list", page=1))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 添加电影
@admin.route("/movie/add/", methods=["GET", "POST"])
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        #获取filename
        file_url = secure_filename(form.url.data.filename)  # 安全性
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")  # 目录权限
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        movie = Movie(
            title=data["title"],
            url=url,
            info=data["info"],
            logo=logo,
            star=int(data["star"]),
            playnum=0,
            commentnum=0,
            tag_id=int(data["tag_id"]),
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"]
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功", "ok")
        return redirect(url_for('admin.movie_add'))
    return render_template("admin/movie_add.html", form=form)


# 电影列表
@admin.route("/movie/list/<int:page>/", methods=["GET"])
@admin_login_req
def movie_list(page):
    if page is None:
        page = 1
    # 外键关联
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime
    ).paginate(page=page, per_page=5)  # 传入分页
    return render_template("admin/movie_list.html", page_data=page_data)


# 电影删除
@admin.route("/movie/del/<int:id>/", methods=["GET"])
@admin_login_req
def movie_del(id=None):
    movie = Movie.query.filter_by(id=id).first_or_404()  # 查询不到返回404
    # 或者  Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash("删除电影成功！", "ok")
    return redirect(url_for("admin.movie_list", page=1))


# 编辑电影
@admin.route("/movie/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(id)
    # 表单设置初值
    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")  # 目录权限
        if form.url.data:
            file_url = secure_filename(form.url.data.filename)  # 安全性
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + movie.url)
        if form.logo.data:
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            #文件保存
            form.logo.data.save(app.config["UP_DIR"] + movie.logo)
        data = form.data
        movie.star = data["star"]
        movie.tag_id = data["tag_id"]
        movie.info = data["info"]
        movie.title = data["title"]
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = data["release_time"]
        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功", "ok")
        return redirect(url_for('admin.movie_edit', id=id))
    return render_template("admin/movie_edit.html", form=form, movie=movie)


# 编辑上映预告
@admin.route("/preview/add/",methods=["GET", "POST"])
@admin_login_req
def preview_add():
    form=PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")  # 目录权限
        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        preview = Preview(
            title=data["title"],
            logo=logo,
        )
        db.session.add(preview)
        db.session.commit()
        flash("添加预告成功！", "ok")
        return redirect(url_for('admin.preview_add'))
    return render_template("admin/preview_add.html",form=form)


# 上映预告列表
@admin.route("/preview/list/<int:page>/", methods=["GET"])
@admin_login_req
def preview_list(page):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=5)  # 传入分页
    return render_template("admin/preview_list.html",page_data=page_data)

#删除预告
@admin.route("/preview/del/<int:id>/", methods=["GET"])
@admin_login_req
def preview_del(id=None):
    preview=Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    flash("删除预告成功","ok")
    return redirect(url_for('admin.preview_list',page=1))

#编辑预告
@admin.route("/preview/edit/<int:id>/", methods=["GET","POST"])
@admin_login_req
def preview_edit(id):
    form=PreviewForm()
    preview=Movie.query.get_or_404(id)
    if request.method=="GET":
        form.title.data=preview.title
    if form.validate_on_submit():
        data=form.data
        if form.logo.data:
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            # 文件保存
            form.logo.data.save(app.config["UP_DIR"] + preview.logo)
        preview.title=data["title"]
        db.session.commit()
        flash("修改预告成功！","ok")
        return redirect(url_for('admin.preview_edit',id=id))
    return render_template("admin/preview_edit.html",form=form,preview=preview)


@admin.route("/user/view/")
@admin_login_req
def user_view():
    return render_template("admin/user_view.html")


@admin.route("/user/list/")
@admin_login_req
def user_list():
    return render_template("admin/user_list.html")


@admin.route("/comment/list/")
@admin_login_req
def comment_list():
    return render_template("admin/comment_list.html")


@admin.route("/moviecol/list/")
@admin_login_req
def moviecol_list():
    return render_template("admin/moviecol_list.html")


@admin.route("/oplog/list/")
@admin_login_req
def oplog_list():
    return render_template("admin/oplog_list.html")


@admin.route("/adminloginlog/list/")
@admin_login_req
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")


@admin.route("/userloginlog/list/")
@admin_login_req
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")


@admin.route("/role/add/")
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")


@admin.route("/role/list/")
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")


@admin.route("/auth/add/")
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")


@admin.route("/auth/list/")
@admin_login_req
def auth_list():
    return render_template("admin/auth_list.html")


@admin.route("/admin/add/")
@admin_login_req
def admin_add():
    return render_template("admin/admin_add.html")


@admin.route("/admin/list/")
@admin_login_req
def admin_list():
    return render_template("admin/admin_list.html")
