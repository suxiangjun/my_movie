#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "junesu"
# Date: 2018-07-05
from flask_wtf import FlaskForm
from wtforms import SelectField,TextAreaField,StringField, PasswordField, SubmitField,FileField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin,Movie,Tag
tags=Tag.query.all()

class LoginForm(FlaskForm):
    '''管理员登陆表单'''
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！"
            # "required": "required"  # 前端加入判别
        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！"
            # "required": "required"
        }
    )

    submit = SubmitField(
        '登陆',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在")


class TagForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入标签！")
        ],
        description="标签",
        render_kw={
            "class":"form - control",
            "placeholder": "请输入标签名称！",
            "id":"input_name"

        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn-primary",
        }
    )

class MovieForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名！")
        ],
        description="片名",
        render_kw={
            "class":"form-control",
            "placeholder": "请输入片名！",
            "id":"input_title",

        }
    )
    url=FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件",
    )

    #文本框
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
    logo=FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面",
    )
    #选择框
    star=SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(1,"1星"),(2,"2星"),(3,"3星"),(4,"4星"),(5,"5星")],
        description="星级",
        render_kw={
            "class": "form-control",
        }
    )

    tag_id=SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        choices=[(v.id,v.name) for v in tags],
        description="标签",
        render_kw={
            "class": "form-control",
        }
    )

    #下拉框
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class":"form-control",
            "placeholder": "请输入地区！",
        }
    )

    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长！")
        ],
        description="片长",
        render_kw={
            "class":"form-control",
            "placeholder": "请输入片长！",
        }
    )

    release_time= StringField(
        label="上映时间",
        validators=[
            DataRequired("请输入上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class":"form-control",
            "placeholder": "请选择上映时间！",
            "id":"input_release_time"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn-primary",
        }
    )




class PreviewForm(FlaskForm):
    title=StringField(
        label="预告",
        validators=[
            DataRequired("请输入预告标题！")
        ],
        description="预告",
        render_kw={
            "class":"form-control",
            "placeholder": "请输入预告标题！",
        }
    )
    logo=FileField(
        label="预告封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="预告封面",
    )

    submit = SubmitField(
        '提交',
        render_kw={
            "class": "btn-primary",
        }
    )


















