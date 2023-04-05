from django.shortcuts import render
from products.models import Product, Category
# Create your views here.
 

def index(request):
    context = {
        'products' : Product.objects.filter(active=True),
        'categorys': Category.objects.all(),
        # 'category_length':len(categorys),
        'featured': Product.objects.filter(featured=True),
        'new_items': Product.objects.filter(new_items=True),
        'on_sale': Product.objects.filter(on_sale=True),
        }
    return render(request, 'home/index.html', context)
    

# def index(request):
   

#     feature = Product.objects.all()
#     Product.objects.filter(featured=True)
#     featured = Product.objects.all()

#     context = {
#         'products' : Product.objects.all(),
#         'categorys': Category.objects.all(),
#         'featured': featured

#         }
#         to get featured products
#     return render(request, 'home/index.html', context)