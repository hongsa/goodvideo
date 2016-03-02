# -*- coding: utf-8 -*-
from flask import render_template, session, flash, redirect, url_for, request
from apps import db
from apps.models import Partner, PartnerClick, PartnerPaid
from sqlalchemy import desc
from  sqlalchemy.sql.expression import func


def c_check():
    if not 'partner_id' in session:
        flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
        return redirect(url_for('p_login'))

    if request.method =="POST":
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

        partner = Partner.query.get(session['partner_id'])
        result = partner.click_partner.filter(PartnerClick.created.between(start,end)).add_columns(func.count(PartnerClick.id)) \
            .group_by(func.year(PartnerClick.created),func.month(PartnerClick.created),func.day(PartnerClick.created)).all()

        if result:
            return render_template("cash_check.html",result=result,start=start,end2=end2)
        else:
            flash(u"검색결과가 없습니다.")
            return render_template("cash_check.html")

    return render_template("cash_check.html")

def c_register():
    if not 'partner_id' in session:
        flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
        return redirect(url_for('p_login'))

    partner = Partner.query.get(session['partner_id'])
    total = partner.click_partner.add_columns(func.count(PartnerClick.id)) \
        .group_by(func.year(PartnerClick.created),func.month(PartnerClick.created),func.day(PartnerClick.created)).all()

    total_cash = 0
    for each in total:
        total_cash += int(each[1] * each[0].miss) * each[0].partner.click

    paid1 = partner.paid_partner.filter(PartnerPaid.state==1).with_entities(PartnerPaid.money).all()
    process = partner.paid_partner.filter(PartnerPaid.state==0).with_entities(PartnerPaid.money).all()

    total_paid = 0
    total_process = 0

    for each in paid1:
        total_paid+=each.money

    for each in process:
        total_process+=each.money

    paid = partner.paid_partner.order_by(desc(PartnerPaid.register_date)).limit(10)

    if request.method =="POST":
        money_out = int(request.form['money_out'])
        personal_number = request.form['personal_number']

        if money_out < 10000:
            flash(u"만원 이상만 가능합니다.")
            return redirect(url_for('c_register'))

        elif money_out>int(total_cash-total_paid-total_process):
            flash(u"출금 가능액을 확인해주세요")
            return redirect(url_for('c_register'))

        else:
            paid = PartnerPaid(partner_id = session['partner_id'],money=money_out,personal_number=personal_number)
            db.session.add(paid)
            db.session.commit()

            return redirect(url_for('c_register'))

    return render_template("cash_register.html",total_cash=total_cash,total_process=total_process,total_paid=total_paid,paid=paid)
