from cmath import log
from tkinter import E
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from .models import Profile, CartItem, Cart
from products.models import Product

def activate(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception  as e:
         return HttpResponse ('invalid email token')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.get().is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        else:
            messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html',{})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)

    return render(request ,'accounts/register.html',{})
def logout(request):
    auth.logout(request)
    return redirect('/')


# def cartitem(request):
#     try:
#             cart = CartItem.objects.filter(user=request.user, ordered=False)
#             context = {
#                 'timi': cart
#             }
#             return render(request, 'accounts/cart.html', context)
#     except ObjectDoesNotExist:
#             messages.warning(request, "You do not have an active order")
#             return redirect("/")
@login_required(login_url='login')
def cart(request):
    try:
            cart = Cart.objects.get(user=request.user, ordered=False)
            context = {
                 'object': cart
             }
            return render(request, 'accounts/cart.html', context)
    except ObjectDoesNotExist:
            messages.warning(request, "You do not have an active order")
            return redirect("/")

    # context = {
    # 'cart' : Cart.objects.filter(user=request.user, ordered=False)
    # }

    # return render(request, 'accounts/cart.html', context)
   

def add(request, slug):
        # cart = CartItem.objects.get(user=request.user, ordered=False)
        product = get_object_or_404(Product, slug=slug)
        order_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
        order_qs = Cart.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            cart = order_qs[0]
        # check if the order item is in the order
            if cart.items.filter(product__slug=product.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.success(request, "This item quantity was updated.")
                return redirect("get_product", slug=slug)
            else:
                cart.items.add(order_item)
                messages.success(request, "This item was added to your cart.")
                return redirect("get_product", slug=slug)
        else:
            cart = Cart.objects.create(user=request.user)
            cart.items.add(order_item)
            messages.success(request, "This item was added to your cart.")
            return redirect("get_product", slug=slug)


def remove(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        cart = order_qs[0]
        # check if the order item is in the order
        if cart.items.filter(product__slug=product.slug).exists():
            order_item = CartItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            cart.items.remove(order_item)
            order_item.delete()
            messages.success(request, "This item was removed from your cart.")
            return redirect("get_product", slug=slug)
        else:
            messages.warning(request, "This item was not in your cart")
            return redirect("get_product", slug=slug)
    else:
        messages.warning(request, "You do not have an active order")
        return redirect("get_product", slug=slug)

def remove_item(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        cart = order_qs[0]
        # check if the order item is in the order
        if cart.items.filter(product__slug=product.slug).exists():
            order_item = CartItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                cart.items.remove(order_item)
            messages.success(request, "This item quantity was updated.")
            return redirect("cart", )
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart", )
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart", )
