from django.shortcuts import render
from .models import Product

def index(request):
    allproducts = Product.objects.order_by('p_price')
    context = {
        'allproducts': allproducts
    }
    return render(request, 'shop/index.html', context)
# Create your views here.
