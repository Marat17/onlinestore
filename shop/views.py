from django.shortcuts import render
from .models import Product, Category

def index(request):
    allproducts = Product.objects.order_by('p_price')
    context = {
        'allproducts': allproducts
    }
    return render(request, 'shop/index.html', context)


def show_product(request, product_name_slug):
    context = {}
    try:
        product = Product.objects.get(slug=product_name_slug)
        context['product'] = product
    except Product.DoesNotExist:
        context['product'] = None

    return render(request, 'shop/product.html', context)


def show_category(request, category_name_slug):
    context = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        products = Product.objects.filter(category=category)
        context['products'] = products
        context['category'] = category
    except Category.DoesNotExist:
        context['category'] = None
        context['products'] = None

    return render(request, 'shop/category.html', context)