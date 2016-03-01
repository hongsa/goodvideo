# -*- coding:utf-8 -*-
from apps import db
import json
import urllib
import pytz
import datetime
import httplib
import logging

def get_current_time():
    return datetime.datetime.now(pytz.timezone('Asia/Seoul'))


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.String(255))
    password = db.Column(db.String(255))
    nickname = db.Column(db.String(255),index=True)
    #0은 남자 1은 여자
    sex = db.Column(db.Integer, default = 0)
    joinDATE = db.Column(db.DateTime(),default = get_current_time)
    level = db.Column(db.Integer, default = 0)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255),default=0)
    title = db.Column(db.String(255))
    category = db.Column(db.Integer,default=0)
    click = db.Column(db.Integer,default =0)
    created = db.Column(db.DateTime(), default=get_current_time)
    video_src = db.Column(db.String(255))


class Partner(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    partner_id = db.Column(db.String(255))
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    kakao = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    bank_name = db.Column(db.String(255))
    bank_number = db.Column(db.String(255))
    bank_owner = db.Column(db.String(255))
    #1이면 수수료 없음
    commission = db.Column(db.Float,default=0.80)
    click = db.Column(db.Integer,default=5)

    #0은 남자 1은 여자
    joinDATE = db.Column(db.DateTime(),default = get_current_time)
    level = db.Column(db.Integer, default = 0)


class PartnerClick(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    partner = db.relationship('Partner', backref=db.backref('click_partner', cascade='all, delete-orphan', lazy='dynamic'))
    partner_id = db.Column(db.Integer, db.ForeignKey(Partner.id))
    video = db.relationship('Video', backref=db.backref('click_video', cascade='all, delete-orphan', lazy='dynamic'))
    video_id = db.Column(db.Integer, db.ForeignKey(Video.id))
    created = db.Column(db.DateTime(), default=get_current_time)
    miss = db.Column(db.Float)
    ip = db.Column(db.String(255))


class PartnerPaid(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    partner = db.relationship('Partner', backref=db.backref('paid_partner', cascade='all, delete-orphan', lazy='dynamic'))
    partner_id = db.Column(db.Integer, db.ForeignKey(Partner.id))
    register_date = db.Column(db.DateTime(),default = get_current_time)
    paid_date = db.Column(db.DateTime(),default=0)
    money = db.Column(db.Integer, default=0)
    state = db.Column(db.Integer, default=0)
    personal_number = db.Column(db.String(255))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner = db.relationship('Partner', backref=db.backref('question_partner', cascade='all, delete-orphan', lazy='dynamic'))
    partner_id = db.Column(db.Integer, db.ForeignKey(Partner.id))
    title = db.Column(db.String(120))
    content = db.Column(db.Text())
    click = db.Column(db.Integer,default =0)
    commentCount = db.Column(db.Integer,default =0)
    created = db.Column(db.DateTime(), default=get_current_time)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    partner = db.relationship('Partner', backref=db.backref('answer_partner', cascade='all, delete-orphan', lazy='dynamic'))
    partner_id = db.Column(db.Integer, db.ForeignKey(Partner.id))
    question = db.relationship('Question', backref=db.backref('answer_question', cascade='all, delete-orphan', lazy='dynamic'))
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=get_current_time)

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=get_current_time)
    file = db.Column(db.Text())