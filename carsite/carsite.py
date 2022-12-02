from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from carsite.auth import login_required
from carsite.db import get_db

bp = Blueprint('carsite', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, price, style, make, model, fuel, age, mileage, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('carsite/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        style = request.form['style']
        make = request.form['make']
        model = request.form['model']
        fuel = request.form['fuel']
        age = request.form['age']
        mileage = request.form['mileage']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, price, style, make, model, fuel, age, mileage, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (title, price, style, make, model, fuel, age, mileage, g.user['id'])
            )
            db.commit()
            return redirect(url_for('carsite.index'))

    return render_template('carsite/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, price, style, make, model, fuel, age, mileage, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        style = request.form['style']
        make = request.form['make']
        model = request.form['model']
        fuel = request.form['fuel']
        age = request.form['age']
        mileage = request.form['mileage']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, price = ?, style = ?, make = ?, model = ?, fuel = ?, age = ?, mileage = ?'
                ' WHERE id = ?',
                (title, price, style, make, model, fuel, age, mileage, id)
            )
            db.commit()
            return redirect(url_for('carsite.index'))

    return render_template('carsite/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('carsite.index'))