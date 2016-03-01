# -*- coding: utf-8 -*-
from flask import redirect, url_for, flash, session,render_template,request,jsonify,json,make_response
from apps import app,db
from controller import user
from models import User,Video,Partner,PartnerClick,PartnerPaid,Question,Answer,Notice
from sqlalchemy import desc
import math
import logging
import random
from  sqlalchemy.sql.expression import func
import datetime
import pytz
import os
from werkzeug.security import generate_password_hash, check_password_hash


def get_current_time():
    return datetime.datetime.now(pytz.timezone('Asia/Seoul'))

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():

    video={}
    video['issue'] = Video.query.filter_by(category=1).order_by(desc(Video.created)).limit(8)
    video['red'] = Video.query.filter_by(category=2).order_by(desc(Video.created)).limit(8)
    video['entertain'] = Video.query.filter_by(category=3).order_by(desc(Video.created)).limit(8)
    video['humor'] = Video.query.filter_by(category=4).order_by(desc(Video.created)).limit(8)
    video['game'] = Video.query.filter_by(category=5).order_by(desc(Video.created)).limit(8)
    video['sport'] = Video.query.filter_by(category=6).order_by(desc(Video.created)).limit(8)
    video['beauty'] = Video.query.filter_by(category=7).order_by(desc(Video.created)).limit(8)
    video['fight'] = Video.query.filter_by(category=8).order_by(desc(Video.created)).limit(8)
    video['accident'] = Video.query.filter_by(category=9).order_by(desc(Video.created)).limit(8)
    today = Video.query.order_by(desc(Video.click)).limit(4)

    return render_template("index.html",video=video,today=today)

    # return render_template("error.html")

# @app.errorhandler(Exception)
# def page_not_found(e):
#
#     logging.error(e)
#     return render_template("error.html"), 500


@app.route('/<int:filter>',defaults={'page':1})
@app.route('/<int:filter>/<int:page>',methods=['GET','POST'])
def category(filter,page):

    if filter == 10:
        video = Video.query.order_by(desc(Video.click)).offset((page-1)*16).limit(16)
        total = Video.query.count()
    else:
        video = Video.query.filter_by(category=filter).order_by(desc(Video.created)).offset((page-1)*16).limit(16)
        total = Video.query.filter_by(category=filter).count()

    calclulate = float(float(total) / 16)
    total_page = math.ceil(calclulate)


    a = float(math.ceil(float(page)/10))
    if a ==1:
        down=1
    else:
        down = int((a-1) * 10)

    if total_page > a*10:
        total_page = a * 10
        up = int(total_page+1)

    else:
        up = int(total_page)

    main=""
    if filter ==1:
        main = u"이슈"
    elif filter == 2:
        main = u"레드"
    elif filter == 3:
        main = u"연예"
    elif filter == 4:
        main = u"유머"
    elif filter ==5:
        main = u"게임"
    elif filter== 6:
        main = u"스포츠"
    elif filter== 7:
        main = u"뷰티"
    elif filter== 8:
        main = u"싸움"
    elif filter== 9:
        main = u"사건/사고"
    elif filter==10:
        main = u"베스트"


    return render_template("category.html",video=video,total_page=range(1+(10*(int(a)-1)), int(total_page+1)), up = up, down = down,page=page,filter=filter,main = main)



# 회원가입
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return user.signup()

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    return user.login()

#로그아웃 부분.
@app.route('/logout')
def logout():
    return user.logout()

@app.route('/contact')
def contact():
    return user.contact()

# @app.route('/m_pw', methods=['GET', 'POST'])
# def modify_password():
#     return user.modify_password()

#회원 닉네임 수정
@app.route('/m_nick', methods=['GET', 'POST'])
def modify_nickname():
    return user.modify_nickname()


@app.route('/detail/<int:id>', methods=['GET', 'POST'])
def detail(id):

    video = Video.query.get(id)
    related = Video.query.filter_by(category=video.category).order_by(desc(Video.click)).limit(15)

    video.click+=1

    return render_template("detail.html",video=video,related=related)

@app.route('/admin', methods=['GET', 'POST'])
def admin():

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


@app.route('/partner', methods=['GET', 'POST'])
def partner():

    return render_template("partner.html")
    # return render_template("error.html")

@app.route('/p_signup', methods=['GET', 'POST'])
def p_signup():
    return user.p_signup()

@app.route('/p_login', methods=['GET', 'POST'])
def p_login():
    return user.p_login()

@app.route('/p_logout', methods=['GET', 'POST'])
def p_logout():
    return user.p_logout()


@app.route('/c_check', methods=['GET', 'POST'])
def c_check():
    if not 'partner_id' in session:
        flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
        return redirect(url_for('p_login'))

    if request.method =="POST":
        start_year = request.form['start_year']
        start_month = request.form['start_month']
        start_day = request.form['start_day']

        start = start_year+'-'+start_month+'-'+start_day
        logging.error(start)

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

@app.route('/c_register', methods=['GET', 'POST'])
def c_register():
    if not 'partner_id' in session:
        flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
        return redirect(url_for('p_login'))

    partner = Partner.query.get(session['partner_id'])
    total = partner.click_partner.add_columns(func.count(PartnerClick.id)) \
        .group_by(func.year(PartnerClick.created),func.month(PartnerClick.created),func.day(PartnerClick.created)).all()

    # total_cash = int(total * partner.click * partner.commission)
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

        if money_out <10000:
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

@app.route('/admin_partner', methods=['GET', 'POST'])
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
            # logging.error("4")
            flash(u"검색어를 입력해주세요")


        return render_template("admin_partner.html",partner=partner)

    partner = Partner.query.all()

    return render_template("admin_partner.html",partner=partner)

@app.route('/admin_cash', methods=['GET', 'POST'])
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
        result=[]
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

@app.route('/admin_out', methods=['GET', 'POST'])
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

        end_month2=""

        if end_day2 == '32':
            if end_month == '12':
                end_month = '1'
            else:
                end_month = str(int(end_month)+1)
            end_day2 ='1'

        end = end_year+'-'+end_month+'-'+end_day2
        end2 = end_year+'-'+end_month+'-'+end_day

        result=[]
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


@app.route('/state', methods=['GET', 'POST'])
def state():

    id = request.form.get('id')
    value = request.form.get('value')
    if value =="완료":
        value = 1
    else:
        value = 2

    # logging.error(id)
    # logging.error(value)


    paid = PartnerPaid.query.get(id)
    paid.state = value
    paid.paid_date = get_current_time()
    db.session.commit()

    return jsonify(success=True)

@app.route('/p_modify/<int:id>', methods=['GET', 'POST'])
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


@app.route('/p_delete/<int:id>', methods=['GET', 'POST'])
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

@app.route('/question/<int:page>',defaults={'page':1})
@app.route('/question/<int:page>', methods=['GET', 'POST'])
def question(page):

    if not 'partner_id' in session:
        flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
        return redirect(url_for('p_login'))

    question = Question.query.order_by(desc(Question.created)).offset((page - 1) * 15).limit(15)

    total = Question.query.count()
    calclulate = float(float(total) / 15)
    total_page = math.ceil(calclulate)
    a = float(math.ceil(float(page)/10))
    if a ==1:
        down=1
    else:
        down = int((a-1) * 10)

    if total_page > a*10:
        total_page = a * 10
        up = int(total_page+1)

    else:
        up = int(total_page)

    return render_template("question.html", question=question,total_page=range(1+(10*(int(a)-1)), int(total_page+1)), up = up, down = down,page=page)

@app.route('/q_write', methods=['GET', 'POST'])
def q_write():
    # logging.error(session['partner_id'])

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


@app.route('/q_detail/<int:id>',defaults={'page':1})
@app.route('/q_detail/<int:id>', methods=['GET', 'POST'])
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



@app.route('/answer',methods=['GET', 'POST'])
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

@app.route('/guide',methods=['GET', 'POST'])
def guide():

    return render_template("guide.html")
@app.route('/modify_video/<int:page>',defaults={'page':1})
@app.route('/modify_video/<int:page>',methods=['GET', 'POST'])
def modify_video(page):

    if not 'session_user_id' in session:
        return redirect(url_for('index'))

    if session['session_user_id'] != 1:
        return redirect(url_for('index'))

    if request.method=="POST":
        category = request.form['category']

        result = Video.query.filter_by(category=category).order_by(desc(Video.created)).offset((page-1)*30).limit(30)

        total = Video.query.filter_by(category=category).count()
        calclulate = float(float(total) / 16)
        total_page = math.ceil(calclulate)


        a = float(math.ceil(float(page)/10))
        if a ==1:
            down=1
        else:
            down = int((a-1) * 10)

        if total_page > a*10:
            total_page = a * 10
            up = int(total_page+1)

        else:
            up = int(total_page)

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

        return render_template("modify_video.html",result=result,category=category,total_page=range(1+(10*(int(a)-1)), int(total_page+1)), up = up, down = down,page=page)



    total = Video.query.count()
    calclulate = float(float(total) / 16)
    total_page = math.ceil(calclulate)


    a = float(math.ceil(float(page)/10))
    if a ==1:
        down=1
    else:
        down = int((a-1) * 10)

    if total_page > a*10:
        total_page = a * 10
        up = int(total_page+1)

    else:
        up = int(total_page)
    result = Video.query.order_by(desc(Video.created)).order_by(desc(Video.created)).offset((page-1)*30).limit(30)
    category = u"전체"
    return render_template("modify_video.html",result=result,category=category,total_page=range(1+(10*(int(a)-1)), int(total_page+1)), up = up, down = down,page=page)

@app.route('/delete_video/<int:id>',methods=['GET', 'POST'])
def delete_video(id):

    video = Video.query.get(id)
    db.session.delete(video)
    db.session.commit()

    result = Video.query.order_by(desc(Video.created)).limit(30)
    main = u"전체"

    return render_template("modify_video.html",result=result,main=main)

@app.route('/q_delete/<int:id>',methods=['GET', 'POST'])
def q_delete(id):

    question= Question.query.get(id)
    answer = question.answer_question.all()

    for each in answer:
        db.session.delete(each)

    db.session.delete(question)
    db.session.commit()

    return redirect(url_for('question',page=1))

@app.route('/realclick')
def realclick():
    return render_template("realclick.html")


@app.route('/modify_click',methods=['GET', 'POST'])
def modify_click():

    if request.method=="POST":

        id = request.form['id']
        click = request.form['click']

        video = Video.query.get(id)
        video.click = click

        db.session.commit()


    return redirect(url_for('modify_video',page=1))



@app.route('/notice/<int:page>',defaults={'page':1})
@app.route('/notice/<int:page>', methods=['GET', 'POST'])
def notice(page):

    if not 'partner_id' in session:
        flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
        return redirect(url_for('p_login'))

    notice = Notice.query.order_by(desc(Notice.created)).offset((page - 1) * 15).limit(15)

    total = Notice.query.count()
    calclulate = float(float(total) / 15)
    total_page = math.ceil(calclulate)
    a = float(math.ceil(float(page)/10))
    if a ==1:
        down=1
    else:
        down = int((a-1) * 10)

    if total_page > a*10:
        total_page = a * 10
        up = int(total_page+1)

    else:
        up = int(total_page)

    return render_template("notice.html", notice=notice,total_page=range(1+(10*(int(a)-1)), int(total_page+1)), up = up, down = down,page=page)


@app.route('/n_write', methods=['GET', 'POST'])
def n_write():

    # UPLOAD_FOLDER = '/upload'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    if request.method == "POST":
        # file = request.files['file']
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file))

        this=Notice(
            title = request.form['title'],
            content = request.form['content'],
            # file = request.files['file']
        )

        db.session.add(this)
        db.session.commit()
        return redirect(url_for('notice',page=1))

    return render_template("n_write.html")


@app.route('/n_detail/<int:id>',defaults={'page':1})
@app.route('/n_detail/<int:id>', methods=['GET', 'POST'])
def n_detail(id):

    if not 'partner_id' in session:
        flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
        return redirect(url_for('p_login'))

    detail = Notice.query.get(id)


    return render_template("n_detail.html",detail=detail)


@app.route('/n_delete/<int:id>',methods=['GET', 'POST'])
def n_delete(id):

    notice= Notice.query.get(id)

    db.session.delete(notice)
    db.session.commit()

    return redirect(url_for('notice',page=1))


@app.route('/m_password', methods=['GET', 'POST'])
def modify_password():
    partner = Partner.query.get(session['partner_id'])

    if request.method == 'POST':
        partner.password = generate_password_hash(request.form['password'])
        db.session.commit()
        flash(u"변경 완료되었습니다.", "password")
        return redirect(url_for('modify_password'))

    return render_template("modify.html")


@app.route('/m_info', methods=['GET', 'POST'])
def modify_info():

    if request.method=="POST":

        id = request.form['id']
        category = request.form['category']
        title = request.form['title']
        video_src = request.form['video_src']

        video = Video.query.get(id)
        video.category = category
        video.title = title
        video.video_src = video_src

        db.session.commit()


    return redirect(url_for('modify_video',page=1))