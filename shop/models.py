from django.db import models
from django.template.defaultfilters import slugify

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.p_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.p_name


class ElementInCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)


class Cart(models.Model):
    number_of_products = models.IntegerField(default=0)
    elements = models.ManyToManyField(ElementInCart)
    url = models.URLField()

    def addelement(self, product, amount):
        self.elements += product
        self.number_of_products += amount


class User(models.Model):
    name = models.CharField(max_length=25)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    element = models.ForeignKey(ElementInCart, on_delete=models.CASCADE)