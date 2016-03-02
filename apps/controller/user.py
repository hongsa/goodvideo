# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, request, flash, session
from apps import db
from werkzeug.security import generate_password_hash, check_password_hash
from apps.models import User,Partner
from apps import forms,forms2
import pytz
import datetime

def get_current_time():
    return datetime.datetime.now(pytz.timezone('Asia/Seoul'))


# 회원가입
def signup():
    form = forms.JoinForm()

    try:
        if session['session_user_id']:
            flash(u"이미 회원가입 하셨습니다!", "error")
            return render_template("signup.html", form=form)
    except Exception, e:
        pass


    if request.method == 'POST':
        if User.query.filter_by(user_id=form.id.data).first():
            flash(u"이미 등록된 아이디 입니다!", "error")
            return render_template("signup.html", form=form)
        if User.query.filter_by(nickname=form.nickname.data).first():
            flash(u"이미 사용중인 닉네임입니다!", "error")
            return render_template("signup.html", form=form)
        if not form.validate_on_submit():
            flash(u"올바른 형식으로 입력해주세요!", "error")
            return render_template("signup.html", form=form)

        user = User(user_id = form.id.data, password=generate_password_hash(form.password.data),
                    nickname=form.nickname.data, sex=form.sex.data,joinDATE=get_current_time())

        db.session.add(user)
        db.session.commit()


        # flash(u"회원가입 되셨습니다!")
        session['session_user_id'] = form.id.data
        session['session_user_nickname'] = form.nickname.data

        return redirect(url_for('index'))

    return render_template("signup.html", form=form)



#로그인
def login():
    
    form = forms.LoginForm()

    try:
        if session['session_user_id']:
            flash(u'이미 로그인 하셨습니다!', "error")
            return redirect(url_for('index'))

    except Exception, e:
        pass


    if request.method == "POST":
        if form.validate_on_submit():
            id = form.id.data
            pwd = form.password.data
            user = User.query.filter_by(user_id=id).first()
            if user is None:
                flash(u"존재하지 않는 아이디입니다.", "error")
                return render_template("login.html", form=form)
            elif not check_password_hash(user.password, pwd):
                flash(u"비밀번호가 틀렸습니다!", "error")
                return render_template("login.html", form=form)
            else:
                session.permanent = True
                session['session_user_id'] = user.id
                session['session_user_nickname'] = user.nickname
                return redirect(url_for('index'))


    return render_template("login.html", form=form)

#로그아웃 부분.
def logout():

    if "session_user_id" in session:
        session.clear()
        # flash(u"로그아웃 되었습니다.")
    else:
        flash(u"로그인 되어있지 않습니다.", "error")
    return redirect(url_for('index'))




# 회원가입
def p_signup():
    form = forms2.JoinForm()

    try:
        if session['partner_id']:
            flash(u"이미 회원가입 하셨습니다!", "error")
            return render_template("p_signup.html", form=form)
    except Exception, e:
        pass


    if request.method == 'POST':
        if Partner.query.filter_by(partner_id=form.id.data).first():
            flash(u"이미 등록된 아이디 입니다!", "error")
            return render_template("p_signup.html", form=form)
        if not form.validate_on_submit():
            flash(u"올바른 형식으로 입력해주세요!", "error")
            return render_template("p_signup.html", form=form)

        partner = Partner(partner_id = form.id.data, password=generate_password_hash(form.password.data),
                    name=form.name.data,kakao=form.kakao.data,phone=form.phone.data,
                    bank_name=form.bank_name.data,bank_number=form.bank_number.data,bank_owner=form.bank_owner.data,
                    joinDATE=get_current_time())

        db.session.add(partner)
        db.session.commit()


        # flash(u"회원가입 되셨습니다!")

        session['partner_id'] = partner.id
        session['partner_name'] = form.name.data

        return redirect(url_for('partner'))

    return render_template("p_signup.html", form=form)



#로그인
def p_login():

    form = forms2.LoginForm()

    try:
        if session['partner_id']:
            flash(u'이미 로그인 하셨습니다!', "error")
            return redirect(url_for('partner'))

    except Exception, e:
        pass


    if request.method == "POST":
        if form.validate_on_submit():
            id = form.id.data
            pwd = form.password.data
            partner = Partner.query.filter_by(partner_id=id).first()
            if partner is None:
                flash(u"존재하지 않는 아이디입니다.", "error")
                return render_template("p_login.html", form=form)
            elif not check_password_hash(partner.password, pwd):
                flash(u"비밀번호가 틀렸습니다!", "error")
                return render_template("p_login.html", form=form)
            else:
                session.permanent = True
                session['partner_id'] = partner.id
                session['partner_name'] = partner.name
                return redirect(url_for('partner'))


    return render_template("p_login.html", form=form)

#로그아웃 부분.
def p_logout():

    if "partner_id" in session:
        session.clear()
        # flash(u"로그아웃 되었습니다.")
    else:
        flash(u"로그인 되어있지 않습니다.", "error")
    return redirect(url_for('partner'))
