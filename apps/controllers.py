# -*- coding: utf-8 -*-
from flask import render_template
from apps import app
from controller import main, user, cash, admin, partner, question


# main.py
@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
    return main.index()

@app.route('/detail/<int:id>', methods=['GET', 'POST'])
def detail(id):
    return main.detail(id)

@app.route('/<int:filter>',defaults={'page':1})
@app.route('/<int:filter>/<int:page>',methods=['GET','POST'])
def category(filter,page):
    return main.category(filter,page)



# user.py
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return user.signup()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return user.login()

@app.route('/logout')
def logout():
    return user.logout()

@app.route('/p_signup', methods=['GET', 'POST'])
def p_signup():
    return user.p_signup()

@app.route('/p_login', methods=['GET', 'POST'])
def p_login():
    return user.p_login()

@app.route('/p_logout', methods=['GET', 'POST'])
def p_logout():
    return user.p_logout()



#cash.py
@app.route('/c_check', methods=['GET', 'POST'])
def c_check():
    return cash.c_check()

@app.route('/c_register', methods=['GET', 'POST'])
def c_register():
    return cash.c_register()



#admin.py
@app.route('/admin', methods=['GET', 'POST'])
def admin_input_video():
    return admin.admin_input_video()

@app.route('/admin_partner', methods=['GET', 'POST'])
def admin_partner():
    return admin.admin_partner()

@app.route('/admin_cash', methods=['GET', 'POST'])
def admin_cash():
    return admin.admin_cash()

@app.route('/admin_out', methods=['GET', 'POST'])
def admin_out():
    return admin.admin_out()

@app.route('/state', methods=['GET', 'POST'])
def state():
    return admin.state()

@app.route('/modify_video/<int:page>',defaults={'page':1})
@app.route('/modify_video/<int:page>',methods=['GET', 'POST'])
def admin_modify_video(page):
    return admin.admin_modify_video(page)

@app.route('/delete_video/<int:id>',methods=['GET', 'POST'])
def admin_delete_video(id):
    return admin.admin_delete_video(id)



#partner.py
@app.route('/partner', methods=['GET', 'POST'])
def partner():
    return render_template("partner.html")

@app.route('/p_modify/<int:id>', methods=['GET', 'POST'])
def p_modify(id):
    return partner.p_modify(id)

@app.route('/p_delete/<int:id>', methods=['GET', 'POST'])
def p_delete(id):
    return partner.p_delete(id)



#question.py
@app.route('/question/<int:page>',defaults={'page':1})
@app.route('/question/<int:page>', methods=['GET', 'POST'])
def question_list(page):
    return question.question_list(page)

@app.route('/q_write', methods=['GET', 'POST'])
def q_write():
    return question.q_write()

@app.route('/q_detail/<int:id>',defaults={'page':1})
@app.route('/q_detail/<int:id>', methods=['GET', 'POST'])
def q_detail(id):
    return question.q_detail(id)

@app.route('/answer',methods=['GET', 'POST'])
def answer():
    return question.answer()

@app.route('/q_delete/<int:id>',methods=['GET', 'POST'])
def q_delete(id):
    return question.q_detail(id)



@app.route('/guide',methods=['GET', 'POST'])
def guide():
    return render_template("guide.html")

@app.route('/realclick')
def realclick():
    return render_template("realclick.html")



# remove fuction

# @app.route('/notice/<int:page>',defaults={'page':1})
# @app.route('/notice/<int:page>', methods=['GET', 'POST'])
# def notice(page):
#
#     if not 'partner_id' in session:
#         flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
#         return redirect(url_for('p_login'))
#
#     notice = Notice.query.order_by(desc(Notice.created)).offset((page - 1) * 15).limit(15)
#
#     total = Notice.query.count()
#     calclulate = float(float(total) / 15)
#     total_page = math.ceil(calclulate)
#     a = float(math.ceil(float(page)/10))
#     if a ==1:
#         down=1
#     else:
#         down = int((a-1) * 10)
#
#     if total_page > a*10:
#         total_page = a * 10
#         up = int(total_page+1)
#
#     else:
#         up = int(total_page)
#
#     return render_template("notice.html", notice=notice,total_page=range(1+(10*(int(a)-1)), int(total_page+1)), up = up, down = down,page=page)
#
#
# @app.route('/n_write', methods=['GET', 'POST'])
# def n_write():
#
#     # UPLOAD_FOLDER = '/upload'
#     # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
#
#     if request.method == "POST":
#         # file = request.files['file']
#         # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
#
#         this=Notice(
#             title = request.form['title'],
#             content = request.form['content'],
#             # file = request.files['file']
#         )
#
#         db.session.add(this)
#         db.session.commit()
#         return redirect(url_for('notice',page=1))
#
#     return render_template("n_write.html")
#
#
# @app.route('/n_detail/<int:id>',defaults={'page':1})
# @app.route('/n_detail/<int:id>', methods=['GET', 'POST'])
# def n_detail(id):
#
#     if not 'partner_id' in session:
#         flash(u"회원가입 및 로그인 후, 이용하실 수 있습니다.")
#         return redirect(url_for('p_login'))
#
#     detail = Notice.query.get(id)
#
#
#     return render_template("n_detail.html",detail=detail)
#
#
# @app.route('/n_delete/<int:id>',methods=['GET', 'POST'])
# def n_delete(id):
#
#     notice= Notice.query.get(id)
#
#     db.session.delete(notice)
#     db.session.commit()
#
#     return redirect(url_for('notice',page=1))
#
#
# @app.route('/m_password', methods=['GET', 'POST'])
# def modify_password():
#     partner = Partner.query.get(session['partner_id'])
#
#     if request.method == 'POST':
#         partner.password = generate_password_hash(request.form['password'])
#         db.session.commit()
#         flash(u"변경 완료되었습니다.", "password")
#         return redirect(url_for('modify_password'))
#
#     return render_template("modify.html")
#
#
# @app.route('/m_info', methods=['GET', 'POST'])
# def modify_info():
#
#     if request.method=="POST":
#
#         id = request.form['id']
#         category = request.form['category']
#         title = request.form['title']
#         video_src = request.form['video_src']
#
#         video = Video.query.get(id)
#         video.category = category
#         video.title = title
#         video.video_src = video_src
#
#         db.session.commit()
#
#
#     return redirect(url_for('modify_video',page=1))