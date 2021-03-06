from datetime import datetime

from flask_login import login_required, current_user
from flask import render_template, Blueprint, flash, redirect, url_for

from project import db
from project.forms.order import OrderForm
from project.models.order import Order

orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders',
                             template_folder='templates')


@orders_blueprint.route('/')
@login_required
def order_list():
    orders = Order.query.order_by('date_order_placed').all()
    return render_template('order_list.html', title='Заказы', orders=orders)


@orders_blueprint.route('/edit/<entity_id>', methods=['GET', 'POST'])
@login_required
def order_edit(entity_id):
    order = Order.query.filter_by(id=entity_id).first_or_404()
    form = OrderForm(obj=order)
    if form.validate_on_submit():
        form.populate_obj(order)
        db.session.add(order)
        db.session.commit()
        flash('Изменения были сохранены', 'success')
        return redirect(url_for('orders.order_list'))
    return render_template('order_edit.html', title=order, form=form)


@orders_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def order_new():
    order = Order(date_order_placed=datetime.now())
    form = OrderForm(obj=order)
    if form.validate_on_submit():
        form.populate_obj(order)
        order.user_id = current_user.id
        db.session.add(order)
        db.session.commit()
        flash('Заказ успешно создан', 'success')
        return redirect(url_for('orders.order_list'))
    return render_template('order_edit.html',
                           title=f'{order.ENTITY_NAME} (Новый)', form=form)
