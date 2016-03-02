# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from apps import db
from apps.models import Partner


def p_modify(id):

    partner = Partner.query.get(id)

    if request.method=="POST":

        commission = float(request.form['commission']) * 0.01
        click = request.form['click']
        bank_name = request.form['bank_name']
        bank_number = request.form['bank_number']
        bank_owner = request.form['bank_owner']

        partner.commission = float(commission)
        partner.click = click
        partner.bank_name = bank_name
        partner.bank_number = bank_number
        partner.bank_owner = bank_owner

        db.session.commit()
        return redirect(url_for('admin_partner'))

    return render_template("p_modify.html",partner=partner)

def p_delete(id):

    partner = Partner.query.get(id)
    click = partner.click_partner.all()
    paid = partner.paid_partner.all()

    for each in paid:
        db.session.delete(each)
    for each in click:
        db.session.delete(each)

    db.session.delete(partner)
    db.session.commit()

    return render_template("admin_partner.html")
