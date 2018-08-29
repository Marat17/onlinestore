from .models import Cart, Category


def cart(request):
    return {'cart': Cart(request)}


def allcategories(request):
    return {'allcategories': Category.objects.all()}
