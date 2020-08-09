from io import BytesIO

import braintree
import weasyprint
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from cart.cart import Cart
from orders.models import Order
from shop.models import Product
from shop.recommender import Recommender


def payment_process(request):
    # Backup Cart
    backup_cart = request.session['backup_cart']
    cart = Cart(request)
    for bc in backup_cart:
        cart.add(get_object_or_404(Product, id=bc['product_id']), bc['quantity'], True)

    # Deal with
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # Get token
        nonce = request.POST.get('payment_method_nonce', None)
        # Transaction Info
        result = braintree.Transaction.sale(
            {
                'amount': '{:2f}'.format(order.get_total_cost()),
                'payment_method_nonce': nonce,
                'options': {
                    'submit_for_settlement': True,
                }
            }
        )
        if result.is_success:
            # Clean Cart
            cart.clear()
            # Clean Coupon
            request.session['coupon_id'] = None

            # Succeed
            order.paid = True
            # Save Transaction ID
            order.braintree_id = result.transaction.id
            order.save()

            # Update Recommend Rank
            r = Recommender()
            order_items = [order_item.product for order_item in order.items.all()]
            r.products_bought(order_items)

            # Create Mail with PDF Invoice
            subject = 'My Shop - Invoice no. {}'.format(order.id)
            message = 'Please, find attached the invoice for your recent purchase.'
            email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

            # Gen. PDF
            html = render_to_string('orders/order/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

            # attach PDF to Mail
            email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')

            # Send Mail
            email.send()

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')

    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')