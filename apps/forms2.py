# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField,SelectField
from wtforms import validators
from wtforms.fields.html5 import EmailField

class JoinForm(Form):
    id = StringField(
        u'아이디',
        [validators.data_required(u'아이디를 입력해주세요.')],
        description={'placeholder': u'자신의 아이디를 정확히 입력해주세요.'}
    )

    password = PasswordField(
        u'비밀번호',
        [validators.data_required(u'비밀번호를 입력해주세요.'),
         validators.EqualTo('confirm_password', message=u'비밀번호가 일치하지 않습니다!')],
        description={'placeholder': u'비밀번호!'}
    )
    confirm_password = PasswordField(
        u'비밀번호 확인',
        [validators.data_required(u'패스워드를 한번 더 입력하세요.')],
        description={'placeholder': u'한번 더!'}
    )
    name = StringField(
        u'이름',
        [validators.data_required(u'이름을 입력해주세요.'),validators.length(max=7)],
        description={'placeholder': u'이름을 입력해주세요.'}
    )

    kakao = StringField(
        u'카카오톡아이디',
        [validators.data_required(u'카톡아이디를 입력해주세요.')],
        description={'placeholder': u'등록하실 카톡아이디!'}
    )

    phone = StringField(
        u'핸드폰번호',
        [validators.data_required(u'핸드폰 번호를 입력해주세요.')],
        description={'placeholder': u'핸드폰 번호를 입력해주세요.'}
    )

    bank_name = StringField(
        u'은행명',
        [validators.data_required(u'은행명을 입력해주세요.')],
        description={'placeholder': u'은행명을 입력해주세요.'}
    )
    bank_number = StringField(
        u'계좌번호',
        [validators.data_required(u'계좌번호를 입력해주세요.')],
        description={'placeholder': u'계좌번호를 입력해주세요.'}
    )
    bank_owner = StringField(
        u'예금주',
        [validators.data_required(u'예금주를 입력해주세요.')],
        description={'placeholder': u'예금주를 입력해주세요.'}
    )


class LoginForm(Form):
    id = StringField(
        u'아이디',
        [validators.data_required(u'아이디를 입력해주세요.')],
        description={'placeholder': u'아이디 입력하기!'}
    )
    password = PasswordField(
        u'비밀번호',
        [validators.data_required(u'비밀번호를 입력해주세요.')],
        description={'placeholder': u'비밀번호!'}
    )