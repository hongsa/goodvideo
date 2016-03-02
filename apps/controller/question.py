# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash, json
from apps import db
from apps.models import Partner, Question, Answer
from apps.controller.pagination import pagination
from sqlalchemy import desc


def question_list(page):

    if not 'partner_id' in session:
        flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
        return redirect(url_for('p_login'))

    question = Question.query.order_by(desc(Question.created)).offset((page - 1) * 15).limit(15)

    total = Question.query.count()
    paging = pagination(total,page)
    up = paging.up()
    down = paging.down()
    total_page = paging.totalCount()

    return render_template("question.html", question=question,total_page=total_page, up = up, down = down, page=page)

def q_write():

    if request.method == "POST":

        this=Question(
            partner_id = session['partner_id'],
            title = request.form['title'],
            content = request.form['content']
        )

        db.session.add(this)
        db.session.commit()
        return redirect(url_for('question',page=1))

    return render_template("q_write.html")


def q_detail(id):

    if not 'partner_id' in session:
        flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
        return redirect(url_for('p_login'))

    detail = Question.query.get(id)

    if detail.partner_id == session['partner_id'] or session['partner_id'] == 1:
        detail.click+=1
        db.session.commit()

        answer = detail.answer_question.all()

        return render_template("q_detail.html",detail=detail,answer=answer)
    else:
        return redirect(url_for('question',page=1))

def answer():

    if request.method == 'POST':
        partner = Partner.query.get(session['partner_id'])
        name = partner.name

        comment = request.form['comment']
        id = request.form['id']
        answer=Answer(
            question_id = id,
            partner_id=session['partner_id'],
            content=comment
        )
        #댓글 DB에 저장
        jsonDict = {}
        jsonDict['partner']=name
        jsonDict['comments'] = comment
        jsonDict['boardId'] = id

        question = Question.query.get(id)
        question.commentCount+=1
        db.session.add(answer)
        db.session.commit()

        return json.dumps(jsonDict)


def q_delete(id):

    question= Question.query.get(id)
    answer = question.answer_question.all()

    for each in answer:
        db.session.delete(each)

    db.session.delete(question)
    db.session.commit()

    return redirect(url_for('question',page=1))