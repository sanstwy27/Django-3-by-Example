import copy

from django.conf import settings
from django.shortcuts import get_object_or_404

from coupons.models import Coupon
from shop.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session

        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

        # store cart
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Empty Cart
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()


    def save(self):
        self.session.modified = True


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def __iter__(self):
        product_ids = self.cart.keys()
        # Get Products
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None


    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / float('100')) * self.get_total_price()
        return float('0')


    def get_total_price_after_diccount(self):
        return self.get_total_price() - self.get_discount()