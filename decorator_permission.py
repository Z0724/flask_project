from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for

# 沒加裝飾器的話所取得的module與name就會是該裝飾器的資訊
def decorator_permission(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user._get_current_object().check_author(func.__module__, func.__name__):
            flash('Good Job')
            return func(*args, **kwargs)
        else:
            flash('你沒有權限喔, 請洽管理員!')
            return redirect(url_for('index'))
    return wrapper

# 在需要加權限的路由下面放@decorator_permission
# 權限的設置規則如下
# 權限名稱範例 newproject.blog.view.read_blog_post
# newproject + 分割路由(有的話)) + view + 頁面路由名稱