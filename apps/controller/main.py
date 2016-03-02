# -*- coding: utf-8 -*-
from flask import render_template
from apps.models import Video
from apps.controller.pagination import pagination
from sqlalchemy import desc

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

def detail(id):

    video = Video.query.get(id)
    related = Video.query.filter_by(category=video.category).order_by(desc(Video.click)).limit(15)
    video.click+=1

    return render_template("detail.html",video=video,related=related)

def category(filter,page):

    if filter == 10:
        video = Video.query.order_by(desc(Video.click)).offset((page-1)*16).limit(16)
        total = Video.query.count()
    else:
        video = Video.query.filter_by(category=filter).order_by(desc(Video.created)).offset((page-1)*16).limit(16)
        total = Video.query.filter_by(category=filter).count()

    paging = pagination(total,page)
    up = paging.up()
    down = paging.down()
    total_page = paging.totalCount()


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


    return render_template("category.html",video=video,
                           total_page=total_page, up = up, down = down, page=page, filter=filter, main = main)


