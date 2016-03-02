# -*- coding: utf-8 -*-
from flask import render_template, flash, request, jsonify, session, redirect, url_for
from apps import db
from apps.models import Partner, PartnerClick, PartnerPaid, Video
from apps.controller.pagination import pagination
from sqlalchemy import desc
from  sqlalchemy.sql.expression import func
import datetime
import pytz

def get_current_time():
    return datetime.datetime.now(pytz.timezone('Asia/Seoul'))

def admin_input_video():

    if not 'session_user_id' in session:
        return redirect(url_for('index'))

    if session['session_user_id'] != 1:
        return redirect(url_for('index'))

    if request.method=="POST":

        name = request.form['name']
        video_src = request.form['video_src']
        category = request.form['category']

        video=Video(title=name,video_src=video_src,category=category)
        db.session.add(video)
        db.session.commit()

        flash("성공")
        return redirect(url_for('admin'))

    return render_template("admin.html")

def admin_partner():

    if request.method=="POST":

        id = request.form['id']
        name = request.form['name']

        partner=[]
        if id == "" and name!="":
            partner = Partner.query.filter_by(name = name).all()
        elif name == "" and id != "":
            partner = Partner.query.filter_by(partner_id = id).all()
        elif id and name != "":
            partner = Partner.query.filter_by(partner_id = id,name=name).all()
        else:
            flash(u"검색어를 입력해주세요")

        return render_template("admin_partner.html",partner=partner)

    partner = Partner.query.all()
    return render_template("admin_partner.html",partner=partner)

def admin_cash():

    if request.method=="POST":

        id = request.form['id']
        name = request.form['name']
        start_year = request.form['start_year']
        start_month = request.form['start_month']
        start_day = request.form['start_day']
        start = start_year+'-'+start_month+'-'+start_day

        end_year = request.form['end_year']
        end_month = request.form['end_month']
        end_day = request.form['end_day']
        end_day2 = str(int(end_day) + 1)

        if end_day2 == '32':
            if end_month == '12':
                end_month = '1'
            else:
                end_month = str(int(end_month)+1)
            end_day2 ='1'

        end = end_year+'-'+end_month+'-'+end_day2
        end2 = end_year+'-'+end_month+'-'+end_day


        total_paid = 0
        if id == "" and name!="":
            partner = Partner.query.filter_by(name = name).first()
            result = partner.click_partner.filter(PartnerClick.created.between(start,end)).add_columns(func.count(PartnerClick.id)).group_by(PartnerClick.partner_id).all()
            paid1 = partner.paid_partner.filter(PartnerPaid.state==1).with_entities(PartnerPaid.money).all()
            for each in paid1:
                total_paid+=each.money

        elif name == "" and id != "":
            partner = Partner.query.filter_by(partner_id = id).first()
            result = partner.click_partner.filter(PartnerClick.created.between(start,end)).add_columns(func.count(PartnerClick.id)).group_by(PartnerClick.partner_id).all()
            paid1 = partner.paid_partner.filter(PartnerPaid.state==1).with_entities(PartnerPaid.money).all()
            for each in paid1:
                total_paid+=each.money

        elif id and name != "":
            partner = Partner.query.filter_by(name = name,partner_id=id).first()
            result = partner.click_partner.filter(PartnerClick.created.between(start,end)).add_columns(func.count(PartnerClick.id)).group_by(PartnerClick.partner_id).all()
            paid1 = partner.paid_partner.filter(PartnerPaid.state==1).with_entities(PartnerPaid.money).all()
            for each in paid1:
                total_paid+=each.money

        else:
            result = PartnerClick.query.filter(PartnerClick.created.between(start,end)).add_columns(func.count(PartnerClick.id)) \
                .group_by(PartnerClick.partner_id).all()

        return render_template("admin_cash.html",result=result,total_paid=total_paid,start=start,end2=end2)

    result = PartnerClick.query.add_columns(func.count(PartnerClick.id)).group_by(PartnerClick.partner_id).order_by(desc(PartnerClick.created)).limit(10)
    return render_template("admin_cash.html",result=result)

def admin_out():
    if request.method=="POST":

        id = request.form['id']
        name = request.form['name']
        start_year = request.form['start_year']
        start_month = request.form['start_month']
        start_day = request.form['start_day']
        start = start_year+'-'+start_month+'-'+start_day

        end_year = request.form['end_year']
        end_month = request.form['end_month']
        end_day = request.form['end_day']
        end = end_year+'-'+end_month+'-'+end_day

        end_day2 = str(int(end_day) + 1)


        if end_day2 == '32':
            if end_month == '12':
                end_month = '1'
            else:
                end_month = str(int(end_month)+1)
            end_day2 ='1'

        end = end_year+'-'+end_month+'-'+end_day2
        end2 = end_year+'-'+end_month+'-'+end_day

        if id == "" and name!="":
            partner = Partner.query.filter_by(name = name).first()
            result = partner.paid_partner.filter(PartnerPaid.register_date.between(start,end)).all()

        elif name == "" and id != "":
            partner = Partner.query.filter_by(name = name).first()
            result = partner.paid_partner.filter(PartnerPaid.register_date.between(start,end)).all()

        elif id and name != "":
            partner = Partner.query.filter_by(name = name).first()
            result = partner.paid_partner.filter(PartnerPaid.register_date.between(start,end)).all()

        else:
            result = PartnerPaid.query.filter(PartnerPaid.register_date.between(start,end)).all()

        return render_template("admin_out.html",result=result,start=start,end2=end2)

    result = PartnerPaid.query.order_by(desc(PartnerPaid.register_date)).limit(15)
    return render_template("admin_out.html",result=result)

def state():

    id = request.form.get('id')
    value = request.form.get('value')
    if value =="완료":
        value = 1
    else:
        value = 2

    paid = PartnerPaid.query.get(id)
    paid.state = value
    paid.paid_date = get_current_time()
    db.session.commit()
    return jsonify(success=True)

def admin_modify_video(page):

    if not 'session_user_id' in session:
        return redirect(url_for('index'))

    if session['session_user_id'] != 1:
        return redirect(url_for('index'))

    if request.method=="POST":
        category = request.form['category']

        result = Video.query.filter_by(category=category).order_by(desc(Video.created)).offset((page-1)*30).limit(30)

        total = Video.query.filter_by(category=category).count()
        paging = pagination(total,page)
        up = paging.up()
        down = paging.down()
        total_page = paging.totalCount()

        if category == "1":
            category = u"이슈"
        elif category == "2":
            category = u"레드"
        elif category == "3":
            category = u"예능"
        elif category == "4":
            category = u"유머"
        elif category =="5":
            category = u"게임"
        elif category== "6":
            category = u"스포츠"
        elif category== "7":
            category = u"뷰티"

        return render_template("modify_video.html",result=result,category=category,total_page=total_page, up = up, down = down,page=page)

    total = Video.query.count()
    paging = pagination(total,page)
    up = paging.up()
    down = paging.down()
    total_page = paging.totalCount()
    result = Video.query.order_by(desc(Video.created)).order_by(desc(Video.created)).offset((page-1)*30).limit(30)
    category = u"전체"

    return render_template("modify_video.html",result=result,category=category,total_page=total_page, up = up, down = down,page=page)

def admin_delete_video(id):

    video = Video.query.get(id)
    db.session.delete(video)
    db.session.commit()

    result = Video.query.order_by(desc(Video.created)).limit(30)
    main = u"전체"

    return render_template("modify_video.html",result=result,main=main)




