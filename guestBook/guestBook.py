from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from .db import get_db

bp = Blueprint('guestBook', __name__)

@bp.route('/')
def index():
    # Достаем все публикации из базы данных
    db = get_db()
    posts = db.execute(
        'SELECT id, author_name, body, created'
        ' FROM post '
        ' WHERE approved = 1'
        ' ORDER BY created DESC' # descending
    ).fetchall()
    # Отображаем их
    return render_template('book/index.html', posts=posts)

# GET - открытие страницы или получение данных
# POST - отправка данных со страницы на сервер
@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        author_name = request.form['author_name'] or 'Гость'
        body = request.form['body']

        error = None
        if not body:
            error = 'Текст сообщения обязателен.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (author_name, body)'
                ' VALUES (?, ?)',
                (author_name, body)
            )
            db.commit()
            flash('Сообщение появится на публичной странице, после проверки модерацией.')
            return redirect(url_for('guestBook.index'))

    # Отображаем форму создания публикации
    return render_template('book/create.html')

@bp.route('/admin/secret', methods = ('GET', 'POST'))
def admin_panel():
    db = get_db()
    posts = db.execute(
        'SELECT id, author_name, body, created, approved'
        ' FROM post'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('book/admin.html', posts=posts)

@bp.route('/admin/approve/<int:id>')
def approve(id):
    db = get_db()
    db.execute('UPDATE post SET approved = 1 WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('guestBook.admin_panel'))

@bp.route('/admin/delete/<int:id>')
def delete(id):
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('guestBook.admin_panel'))
