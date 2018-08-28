from django.db import models
from django.template.defaultfilters import slugify
from decimal import Decimal
from django.conf import settings


class Category(models.Model):
    c_name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.c_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.c_name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    p_name = models.CharField(max_length=80)
    p_price = models.IntegerField()
    p_description = models.TextField(max_length=140)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('p_name',)
        index_together = (('id', 'slug'),)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.p_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.p_name


class Cart(models.Model):

        def __init__(self, request):
            """
            Инициализируем корзину
            """
            self.session = request.session
            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
                # save an empty cart in the session
                cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

        def add(self, product, quantity=1, update_quantity=False):
            """
            Добавить продукт в корзину или обновить его количество.
            """
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0,
                                         'price': str(product.p_price)}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save()

        def save(self):
            # Обновление сессии cart
            self.session[settings.CART_SESSION_ID] = self.cart
            # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
            self.session.modified = True

        def remove(self, product):
            """
            Удаление товара из корзины.
            """
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

        def __iter__(self):
            """
            Перебор элементов в корзине и получение продуктов из базы данных.
            """
            product_ids = self.cart.keys()
            # получение объектов product и добавление их в корзину
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                self.cart[str(product.id)]['product'] = product

            for item in self.cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

        def __len__(self):
            """
            Подсчет всех товаров в корзине.
            """
            return sum(item['quantity'] for item in self.cart.values())

        def get_total_price(self):
            """
            Подсчет стоимости товаров в корзине.
            """
            return sum(Decimal(item['price']) * item['quantity'] for item in
                       self.cart.values())

        def clear(self):
            # удаление корзины из сессии
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True
