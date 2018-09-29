# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm  # 表单基类
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, \
    SelectField, SelectMultipleField  # 字符串字段,密码字段,提交字段,上传文件字段
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import *


class Serial_form(FlaskForm):
    """查询批次号"""
    serial_id = StringField(
        label="查询批次号",
        validators=[DataRequired("查询批次号")],
        description="片名",
        render_kw={
            "class": "form-control bk-valign-top",
            "id": "input_Serial_id",
            "placeholder": "请输入查询批次号！"
        }
    )

    url = FileField(
        label="上传单号",
        validators=[
            # 文件必须选择;
            FileRequired(),
            # 指定文件上传的格式;
            FileAllowed(['xlsx', 'csv'], "上传文件格式错误")
        ],
        description="文件",
        render_kw={
            "class": "king-btn king-default king-file-btn king-btn-small bk-mt3 bk-block",

        }

    )

    submit = SubmitField(
        "上传",

    )

    def validate_account(self, field):  # 验证字段validate_字段名
        account = field.data
        serial_id = Express.query.filter_by(serial_id=account).count()
        if serial_id != 0:
            raise ValidationError('批次号已存在，请重新填写')  # 抛出wtforms.validators异常ValidationError




class LoginForm(FlaskForm):
    """登陆表单"""
    user = StringField(  # 账号框
        label="账号",  # 标签
        validators=[  # 验证器
            DataRequired("请输入账号!")
        ],
        description="账号",  # 描述
        render_kw={  # 自定义属性

            "class": "txt_input txt_input2",
            "placeholder": "请输入账号",
            # "required": "required"
        }
    )

    pwd = PasswordField(  # 密码框
        label="密码",
        validators=[
            DataRequired("请输入密码!")
        ],
        description="密码",
        render_kw={  # 自定义属性
            "class": "txt_input",
            "placeholder": "请输入密码",
            # "required": "required"
        }
    )
    submit = SubmitField(  # 提交按钮
        "登陆",
        description="登陆",
        render_kw={  # 自定义属性
            "class": "sub_button",
            "style": "opacity: 0.7"
        }
    )

