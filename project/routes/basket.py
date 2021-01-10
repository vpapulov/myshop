from datetime import datetime

from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user

from project import db
from project.models.basket import BasketItem
from project.models.order import Order, OrderItem

basket_blueprint = Blueprint('basket', __name__, url_prefix='/basket', template_folder='templates')


@basket_blueprint.route('/')
@login_required
def item_list():
    items = BasketItem.query.filter_by(user_id=current_user.id).order_by('id').all()
    return render_template('basket.html', title='Корзина', item_list=items)


@basket_blueprint.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def item_remove(item_id):
    item = BasketItem.query.filter_by(id=item_id).first_or_404()
    if item.user_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('basket.item_list'))


@basket_blueprint.route('/checkout', methods=['POST'])
@login_required
def checkout():
    basket_items = BasketItem.query.filter_by(user_id=current_user.id).all()
    if len(basket_items) == 0:
        return redirect(url_for('basket.item_list'))
    try:
        with db.session.begin() as tran:
            order = Order()
            order.date_order_placed = datetime.now()
            order.user_id = current_user.id
            order.customer_id = current_user.customer_id
            tran.commit()
            for basket_item in basket_items:
                order_item = OrderItem()
                order_item.order_id = order.id
                order_item.product_id = basket_item.product_id
                order_item.quantity = basket_item.quantity
                order_item.price = 0
                order_item.amount = 0
                tran.add(order_item)
                tran.delete(basket_item)
            flash('Заказ успешно оформлен', 'success')
        return redirect(url_for('product.product_list'))
    except Exception as exc:
        flash(str(exc), 'error')
        flash('Ошибка создания заказа', 'error')
        return redirect(url_for('basket.item_list'))
