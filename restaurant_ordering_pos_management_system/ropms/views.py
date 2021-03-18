from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy 
from django.db.models import Q, Avg, Count, Sum, F, FloatField
from django.db import IntegrityError
from django.contrib import messages
from ropms import models, forms
from functools import wraps

from django.contrib.auth.decorators import login_required 
import json
# Create your views here.

# Decorator
def email_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            email = models.Customer.objects.all().get(Q(email=request.session.get('customer_email', False)) & Q(is_valid=True)) 

            kwargs['email'] = email
        except models.Customer.DoesNotExist:
            return HttpResponseRedirect(reverse("ropms:index_client"))
        return function(request,  *args, **kwargs) 
    return wrap

# Main Views 
def index_client(request):
    template_name = "client/index.html"  
    if request.method == 'POST':
        email_address = request.POST.get("email") 
        try:
            email = models.Customer.objects.all().get(Q(email=email_address)) 
            if email.is_valid:
                request.session['customer_email'] = email.email 
                request.session.set_expiry(600)
                return  HttpResponseRedirect(reverse("ropms:table_selection"))
            else:
                messages.warning(request, "You account is under aprroval! please wait.")
        except models.Customer.DoesNotExist:
            messages.error(request,  "Your email has not been registered!" )
    context = {  
    }

    return render(request, template_name, context)


def registration(request):
    template_name = "client/registration.html"

    if request.method == 'GET':
        form = forms.CustomerForm(request.GET or None)
    elif request.method == 'POST':
        form = forms.CustomerForm(request.POST or None)
        if form.is_valid():
            form.save() 
            return HttpResponseRedirect(reverse("ropms:index_client"))
    context = {
        'form': form,
    }

    return render(request, template_name, context)


@email_required
def table_selection(request, *args, **kwargs): 
    template_name = "client/table-selection.html"
    if request.method == 'GET':   
        tables = models.CustomerTable.objects.all() 
        context = { 
            'tables': tables,
        }

    return render(request, template_name, context)


@email_required
def menu_selection(request, *args, **kwargs):
    template_name = "client/menu-selection.html"
    table = get_object_or_404(models.CustomerTable, id=kwargs.get('id', None))  
    email = kwargs.get('email', None)
    menu_list = models.Menu.objects.all().filter(Q(status='Available'))

    search_term = request.GET.get('search')
    if search_term:
        menu_list = menu_list.filter(Q(name__icontains=search_term) | Q(category__icontains=search_term))
    
    try:
        waiting = models.Waiting.objects.all().get(Q(table=table))
        if  waiting.customer == email:
            
            context = { 
                'waiting': waiting,
                'menu_list': menu_list,
            }
            return render(request, template_name, context)
        else:
            
            messages.error(request, "This table is already occupied by another customer")
            return HttpResponseRedirect(reverse("ropms:table_selection"))
    except models.Waiting.DoesNotExist:
        try:
            waiting = models.Waiting.objects.create(customer=email, table=table)
            table.status = 'Occupied'
            table.save() 
            context = {
                'waiting': waiting,
                'menu_list': menu_list,
            }
            return render(request, template_name, context)
        except IntegrityError:
            messages.error(request, "This table is already occupied by another customer or you are still been assigned on a different table. Please make sure to cancel your table selection first before transfering to a different table.")
            return HttpResponseRedirect(reverse("ropms:table_selection")) 


@email_required
def cancel_table_selection(request, *args, **kwargs): 
    waiting = get_object_or_404(models.Waiting, id=kwargs.get('id', None)) 
    table = get_object_or_404(models.CustomerTable, id=waiting.table.id)
    table.status = "Unoccupied"
    table.save()
    waiting.delete()
    messages.success(request, "You had been successfully canceled your table selection. You may now select a new table!")
    return HttpResponseRedirect(reverse("ropms:table_selection"))

@email_required
def menu_detail(request, *args, **kwargs):
    template_name = "client/menu-detail.html" 
    table = get_object_or_404(models.CustomerTable, id=kwargs.get('tid', None))  
    menu = get_object_or_404(models.Menu, Q(status='Available'), id=kwargs.get('id', None)) 
    related_menu = models.Menu.objects.all().filter(Q(category=menu.category)).exclude(Q(id=menu.id)) 

  
    context = {
        'menu': menu,
        'related_menu': related_menu,
        'table': table,
        'customer': kwargs.get('email',None),
    }
    return render(request, template_name, context)

@email_required
def cart(request, *args, **kwargs):
    # https://docs.djangoproject.com/en/3.1/topics/db/aggregation/ 
    template_name = "client/cart.html" 
    # id = kwargs.get('id',None)
    cid = kwargs.get('email', None)
    tid = kwargs.get('tid',None)
    waiting = get_object_or_404(models.Waiting, customer__id=cid.id, table__id=tid)
    cart = models.Cart.objects.all().filter(Q(customer__id=cid.id)).order_by('-id')

    total_quantity = cart.aggregate(total=Sum('quantity'))['total'] 
    total_quantity = total_quantity if total_quantity != None else 0 
    total_amount = cart.aggregate(total=Sum(F('quantity') * F('menu_item__price'), output_field=FloatField()))['total'] 
    total_amount = total_amount if total_amount != None else 0  
 
    context = {
        'waiting': waiting,
        'cart': cart, 
        'total_quantity': total_quantity,
        'total_amount': float(total_amount),
    }
    return render(request, template_name, context)

@email_required
def add_item_to_cart(request, *args, **kwargs):
    data = dict() 
    if request.is_ajax():
        if request.method == 'POST':
            customer = get_object_or_404(models.Customer, id=kwargs.get('email',None).id)
            menu_item = get_object_or_404(models.Menu, id=kwargs.get('mid', None))

            json_request = request.body
            json_request= json.loads(json_request)
            quantity = json_request['quantity'] 
            # cart, not_created = models.Cart.objects.get_or_create(customer=customer, menu_item=menu_item,  defaults={
            #     'quantity': quantity,
            # }) 
            cart, not_created = models.Cart.objects.get_or_create(customer=customer, menu_item=menu_item) 
            # cart.quantity += int(quantity)
            cart.quantity = F('quantity') + quantity
            cart.save()
            # cart, not_created = models.Cart.objects.update_or_create(customer=customer, menu_item=menu_item, defaults={
            #     'quantity': 2,
            # }) 

            total_all_quantity, total_all_amount, cart = get_results(customer) 

            data['context'] = { 
                'total_all_quantity': total_all_quantity,
                'total_all_amount': total_all_amount,
            }
        return JsonResponse(data)
    else:
        raise Http404()

@email_required
def update_item_to_cart(request, *args, **kwargs):
    data = dict()
    customer = get_object_or_404(models.Customer, id=kwargs.get('email',None).id)
    menu_item = get_object_or_404(models.Menu, id=kwargs.get('mid', None))
    if request.is_ajax():
        if request.method == 'POST':
            json_response = request.body
            json_response = json.loads(json_response)
            quantity = json_response['quantity']
            cart_item, not_created = models.Cart.objects.update_or_create(customer=customer, menu_item=menu_item, defaults={
                'quantity': quantity,
            })  
            total_amount = cart_item.quantity * cart_item.menu_item.price 

            total_all_quantity, total_all_amount, cart = get_results(customer) 
             
            data['context'] = {
                'total_amount': total_amount,
                'total_all_quantity': total_all_quantity,
                'total_all_amount': total_all_amount,
            }
        return JsonResponse(data)
    else:
        raise Http404()
    
@email_required
def delete_item_from_the_cart(request, *args, **kwargs):
    data = dict()
 
    if request.is_ajax():
        if request.method == 'POST':
            customer = get_object_or_404(models.Customer, id=kwargs.get('email',None).id)
            cart = get_object_or_404(models.Cart, id=kwargs.get('cid', None))
            
            cart.delete()

            total_all_quantity, total_all_amount, cart = get_results(customer) 
             
            data['context'] = { 
                'total_all_quantity': total_all_quantity,
                'total_all_amount': total_all_amount,
                'count': cart.count(),
            }
            return JsonResponse(data)
    else:
        raise Http404()

def get_results(customer):

    cart = models.Cart.objects.all().filter(Q(customer=customer)).order_by('-id')
    total_all_quantity = cart.aggregate(total=Sum('quantity'))['total'] 
    total_all_quantity = total_all_quantity if total_all_quantity != None else 0
    total_all_amount = cart.aggregate(total=Sum(F('quantity') * F('menu_item__price'), output_field=FloatField()))['total'] 
    total_all_amount = total_all_amount if total_all_amount != None else 0

    return total_all_quantity, float(total_all_amount), cart


@email_required
def checkout(request, *args, **kwargs): 
    data = dict()
    customer = get_object_or_404(models.Customer, id=kwargs.get('email',None).id) 
    if request.is_ajax():
        if request.method == "POST":
            json_response = request.body
            json_response = json.loads(json_response)
            payment = json_response['payment']

            total_all_quantity, total_all_amount, cart = get_results(customer) 
            change = float(payment) - total_all_amount

            if change < 0:
                data['valid'] = False
            else:

                all_order = models.Cart.objects.all().filter(Q(customer=customer))
                table = get_object_or_404(models.Waiting, customer__id=kwargs.get('email', None).id) 
                for order in all_order:
                    pos = models.POS.objects.create(
                        customer_name=customer,
                        table_name=table.table,
                        menu_name=order.menu_item.name,
                        price=order.menu_item.price,
                        quantity=order.quantity,
                        total=float(order.quantity) * float(order.menu_item.price)
                        )  
                data['valid'] = True    
                data['context'] = {
                    'change': change,
                    'url': str(redirect("ropms:index_client").url),
                }
                del request.session['customer_email']
                request.session.modified = True 
                table.table.status = "Unoccupied"
                table.table.save()
               
                customer.delete()
             
        return JsonResponse(data)
    else:
        raise Http404()



@login_required
def admin_pos_dashboard(request):
    template_name = "admin/admin_pos_dashboard.html"
    pos = models.POS.objects.all()
    total = pos.aggregate(total=Sum('total'))['total']  
    total_quantity = pos.aggregate(total=Sum('quantity'))['total']  
    context ={
        'pos': pos,
        'total': float(total),
        'total_quantity': total_quantity,
    }
    return render(request, template_name, context)