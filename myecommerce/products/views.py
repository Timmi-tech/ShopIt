from django.shortcuts import render
from tkinter import E
from products.models import Product
from django.http import HttpResponseRedirect,HttpResponse

# Create your views here.

def get_product(request, slug):
        product = Product.objects.get(slug =slug)
#     if product == Product.objects.get(slug =slug):
        return render(request  , 'product/product.html' , context = {'product' : product})

#     else: 
#             return HttpResponse ('invalid email token')


        
    