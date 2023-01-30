from flask import render_template, flash, redirect, url_for, request
from newproject.blog.form import Form_Blog_Main, Form_Blog_Post
from newproject.blog.model import Blog_Main, Blog_Post, Blog_Category
from datetime import datetime
from newproject import db
from flask_login import login_required, current_user
from . import blog
from slugify import slugify
from flask_paginate import Pagination, get_page_parameter
from decorator_permission import decorator_permission

# 建立部落格
@blog.route('/blog_main/c',methods=['POST','GET'])
@login_required
def post_blog_main():
    form = Form_Blog_Main()
    if form.validate_on_submit():
        blog = Blog_Main(
            blog_name=form.blog_name.data,
            blog_descri=form.blog_descri.data,
            author=current_user.id
        )
        db.session.add(blog)
        db.session.commit()
        flash('建立部落格完成')
        return redirect(url_for('main.userinfo', username=current_user.username))
    return render_template('blog/blogbook_edit.html', form=form)

        # 也可以利用關聯寫入資料
        # current_user.blog_mains.append(blog)
        # db.session.add(current_user)

# 發文
@blog.route('/blog_post/c', methods=['GET', 'POST'])
@login_required
def post_blog_post():
    form = Form_Blog_Post()

    if form.validate_on_submit():
        post = Blog_Post(
            title=form.post_title.data,
            body=form.post_body.data,
            category=form.post_category.data,
            author=current_user._get_current_object(),
            blog_main=form.post_blog.data,
            slug='%i-%i-%i-%i-%s' % (current_user.id, datetime.now().year, datetime.now().month, datetime.now().day,
                                  slugify(form.post_title.data))
        )
        db.session.add(post)
        db.session.commit()
        flash('發文成功')
        return redirect(url_for('blog.read_blog_post', slug=post.slug))
    return render_template('blog/blog_post_edit.html', form=form)


# 文章列表
@blog.route('/post_list/<blog_id>/')
@blog.route('/post_list/<blog_id>/<int:page>/')
def post_list(blog_id):
    #  加入分頁功能，設置每頁顯示5筆，這部份可以以參數設置
    posts = Blog_Post.query.filter_by(blog_main_id=blog_id).paginate(per_page=5)
    #  利用first_or_404讓系統如果取不到blog的時候就拋出404
    blog = Blog_Main.query.filter_by(id=blog_id).first_or_404()
    return render_template('blog/blog_post_list.html', posts=posts, blog=blog)


# 編輯文章
@blog.route('/blog_post/u/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def update_blog_post(post_id):
    post = Blog_Post.query.filter_by(id=post_id).first_or_404()
    form = Form_Blog_Post()
    if form.validate_on_submit():
        post.title = form.post_title.data
        post.body = form.post_body.data
        print(form.post_body.data)
        post.blog_main_id = form.post_blog.data
        post.category_id = form.post_category.data
        db.session.add(post)
        db.session.commit()
        flash('修改文章成功')
        return redirect(url_for('blog.read_blog_post', slug=post.slug))
    form.post_title.data = post.title
    form.post_body.data = post.body
    form.post_blog.data = post.blog_main_id
    form.post_category.data = post.category_id
    #  利用參數action來做條件，判斷目前是新增還是編輯
    return render_template('blog/blog_post_edit.html', form=form, post=post, action='edit')

# 假設form的filed名稱與model的屬性名稱相同，我們可以直接利用obj渲染，而不用一個一個指定設置
# @blog.route('/blog_post/u/<int:post_id>/', methods=['GET', 'POST'])
# @login_required
# def update_blog_post(post_id):
#     post = Blog_Post.query.filter_by(id=post_id).first_or_404()
#     form = Form_Blog_Post(obj=post)
#     if form.validate_on_submit():
#         form.populate_obj(post)
#         db.session.commit()

@blog.route('/blog_post/r/<slug>/')
@decorator_permission
@login_required
def read_blog_post(slug):
    # if not current_user.check_author('app_blog.blog.view1', 'read_blog_post'):
    #     flash('You Have No Author!')
    #     return redirect(url_for('index'))
    post = Blog_Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/blog_post_read.html', post=post)
