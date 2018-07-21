#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "junesu"
# Date: 2018-07-05
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField,StringField,PasswordField,FileField,TextAreaField
from wtforms.validators import DataRequired,EqualTo,Email,Regexp,ValidationError
from app.models import User
#会员注册表单
class RegistForm(FlaskForm):
    name=StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称！")
        ],
        description="昵称",

        render_kw={
            "class":"form-control input-lg",
            "palaceholder":"请输入昵称！"
        })
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入管理员密码！")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入管理员密码！"
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('pwd',message="密码不一致！")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码！"
        }
    )

    email=StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱地址！"),
            Email("邮箱格式不正确！")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱地址！"
        }
    )

    phone=StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机号码！"),
            Regexp("1[3458]\\d{9}",message="手机格式不正确！")
        ],
        description="手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码！"
        }
    )

    submit = SubmitField(
            '注册',
            render_kw={
                "class": "btn btn-lg btn-success btn-block",
    })

    def validate_name(self,field):
        name=field.data
        user=User.query.filter_by(name=name).count()
        if user==1:
            raise ValidationError("昵称已经存在")

    def validate_email(self,field):
        email=field.data
        user=User.query.filter_by(email=email).count()
        if user==1:
            raise ValidationError("邮箱已经存在")

    def validate_phone(self,field):
        phone=field.data
        user=User.query.filter_by(phone=phone).count()
        if user==1:
            raise ValidationError("手机号已经存在")


class LoginForm(FlaskForm):
    name=StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",

        render_kw={
            "class":"form-control input-lg",
            "palaceholder":"请输入账号！"
        })

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入管理员密码！")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入管理员密码！"
        }
    )

    submit = SubmitField(
            '登陆',
            render_kw={
                "class": "btn btn-lg btn-primary btn-block",
    })

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 0:
            raise ValidationError("账号不存在")


class UserForm(FlaskForm):
    name=StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称！")
        ],
        description="昵称",
        render_kw={
            "class":"form-control",
        })

    email=StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱地址！"),
            Email("邮箱格式不正确！")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control",
        }
    )

    phone=StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机号码！"),
            Regexp("1[3458]\\d{9}",message="手机格式不正确！")
        ],
        description="手机",
        render_kw={
            "class": "form-control",
        }
    )

    face=FileField(
        label="头像",
        validators=[
            DataRequired("请上传头像！")
        ],
        description="头像",
        render_kw={
            "class":"form-control"
        }
    )

    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class":"form-control",
            "rows":10
        }
    )

    submit = SubmitField(
            '保存修改',
            render_kw={
                "class": "btn btn-success",
    })






