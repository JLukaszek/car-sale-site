from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from carsite.auth import login_required
from carsite.db import get_db

bp = Blueprint('carsite', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    makes = ['Audi', 'BMW', 'Citroën', 'Dacia', 'Fiat', 'Ford', 'Hyundai', 'Jeep', 'Kia', 'Mercedes', 'Nissan', 'Opel',
             'Renault', 'Seat', 'Skoda', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo']
    if request.method == "POST":
        make = request.form['make']
        return redirect(url_for('carsite.order_by_make', make=make))
    return render_template('carsite/index.html', makes=makes)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    styles = ['SUV', 'Sedan', 'Coupe', 'Van', 'Hatchback', 'Crossover', 'Truck']
    fuels = ['Gasoline', 'Electric', 'Diesel', 'Hybrid']
    makes = ['Audi', 'BMW', 'Citroën', 'Dacia', 'Fiat', 'Ford', 'Hyundai', 'Jeep', 'Kia', 'Mercedes', 'Nissan', 'Opel',
             'Renault', 'Seat', 'Skoda', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo']
    if request.method == 'POST':
        price = request.form['price']
        style = request.form['style']
        make = request.form['make']
        model = request.form['model']
        fuel = request.form['fuel']
        age = request.form['age']
        mileage = request.form['mileage']

        db = get_db()
        db.execute(
            'INSERT INTO post (price, style, make, model, fuel, age, mileage, author_id)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (price, style, make, model, fuel, age, mileage, g.user['id'])
        )
        db.commit()
        return redirect(url_for('carsite.auctions'))

    return render_template('carsite/create.html', styles=styles, fuels=fuels, makes=makes)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, price, style, make, model, fuel, age, mileage, created, author_id, username'
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
    styles = ['SUV', 'Sedan', 'Coupe', 'Van', 'Hatchback', 'Crossover', 'Truck']
    fuels = ['Gasoline', 'Electric', 'Diesel', 'Hybrid']
    makes = ['Audi', 'BMW', 'Citroën', 'Dacia', 'Fiat', 'Ford', 'Hyundai', 'Jeep', 'Kia', 'Mercedes', 'Nissan', 'Opel',
             'Renault', 'Seat', 'Skoda', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo']
    if request.method == 'POST':
        price = request.form['price']
        style = request.form['style']
        make = request.form['make']
        model = request.form['model']
        fuel = request.form['fuel']
        age = request.form['age']
        mileage = request.form['mileage']

        db = get_db()
        db.execute(
            'UPDATE post SET price = ?, style = ?, make = ?, model = ?, fuel = ?, age = ?, mileage = ?'
            ' WHERE id = ?',
            (price, style, make, model, fuel, age, mileage, id)
        )
        db.commit()
        return redirect(url_for('carsite.auctions'))

    return render_template('carsite/update.html', post=post, styles=styles, fuels=fuels, makes=makes)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('carsite.index'))


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    if request.method == "POST":
        return redirect(url_for('index'))
    return render_template('carsite/account.html')


@bp.route('/auctions', methods=('GET', 'POST'))
def auctions():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, price, style, make, model, fuel, age, mileage, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('carsite/auctions.html', posts=posts)


@bp.route('/auctions/<make>', methods=('GET', 'POST'))
def order_by_make(make):
    db = get_db()
    posts = db.execute(
        'SELECT p.id, price, style, make, model, fuel, age, mileage, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        f' WHERE make = "{make}"'
    ).fetchall()
    return render_template('carsite/order_by_make.html', posts=posts)


@bp.route('/auction/<int:id>', methods=('GET', "POST"))
def single_auction(id):
    post = get_post(id)
    return render_template('carsite/single_auction.html', post=post)
