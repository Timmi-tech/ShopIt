from django.db import models
from timmiemart.models import BaseModel
from django.utils.text import slugify

# Create your models here.


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null = True, blank = True)
    category_image = models.ImageField(upload_to='categories')


    def save(self , *args , **kwargs):
        self.slug = slugify(self.category_name)
        super(Category ,self).save(*args , **kwargs)


    def __str__(self) -> str:
        return self.category_name


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.size_name


# class ProductManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return
#     super().get_queryset(*args, **kwargs).filter(featured=True)
class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null = True, blank = True)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    discount_price = models.IntegerField(null= True, blank=True)
    product_description = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant , blank=True)
    size_variant = models.ManyToManyField(SizeVariant , blank=True)
    featured =models.BooleanField(null= True, blank=True)
    new_items =models.BooleanField(null= True, blank=True)
    on_sale =models.BooleanField(null= True, blank=True)
    active = models.BooleanField(default=True)

    


    def _get_unique_slug(self):
        slug = slugify(self.product_name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug


    def save(self , *args , **kwargs):
        if not self.slug:
           self.slug = self._get_unique_slug()
        super().save(*args , **kwargs)


    def __str__(self) -> str:
        return self.product_name


        def is_featured(self):
            return self.featured

        def is_new_items(self):
            return self.new_items

        def is_on_sale(self):
            return self.on_sale

        def is_active(self):
            return self.active

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product')