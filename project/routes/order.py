from flask_login import login_required
from flask import render_template, Blueprint, request, flash, redirect, url_for

from project import db
from project.forms.order import NewOrderForm, OrderForm
from project.models.order import Order, Customer

orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders', template_folder='templates')


@orders_blueprint.route('/')
@login_required
def order_list():
    orders = Order.query.all()
    return render_template('order_list.html', title='Список заказов', orders=orders)


@orders_blueprint.route('/edit/<order_id>', methods=['GET', 'POST'])
@login_required
def order_edit(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    form = OrderForm(obj=order)
    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
    if form.validate_on_submit():
        form.populate_obj(order)
        db.session.add(order)
        db.session.commit()
        flash('Изменения были сохранены.')
        return redirect(url_for('orders.order_list'))
    return render_template('order_edit.html', title='Заказ ' + order_id, form=form)


@orders_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_order():
    form = NewOrderForm()
    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
    if form.validate_on_submit():
        order = Order()
        form.populate_obj(order)
        db.session.add(order)
        db.session.commit()
        flash('Заказ успешно создан.')
        return redirect(url_for('orders.order_list'))
    return render_template('order_edit.html', title='Новый заказ', form=form)
