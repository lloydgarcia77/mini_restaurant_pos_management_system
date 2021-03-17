from django import template
from ropms import models
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q, F, FloatField
register = template.Library()


@register.simple_tag
def total_amount(quantity, price):
    return quantity * price

@register.inclusion_tag('client/nav_shopping_cart.html')
def nav_shopping_cart(email): 
    customer = get_object_or_404(models.Customer, email=email)
    cart = models.Cart.objects.all().filter(Q(customer__id=customer.id))
    total_quantity = cart.aggregate(total=Sum('quantity'))['total']
    total_amount = cart.aggregate(total=Sum(F('quantity') * F('menu_item__price'), output_field=FloatField()))['total']
    context = {
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    return context