from django.db import models
from django.contrib.auth.models import User
from timmiemart.models import BaseModel
import uuid
# email verfication start here
from django.db.models.signals import post_save
from django.dispatch import receiver
from timmiemart.emails import send_account_activation_email

from products.models import Product
#  ends here

# Create your models here.

class Profile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_img = models.ImageField( upload_to='profile')
#  email verification continues here 
@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance, email_token = email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(e)


class CartItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    # def get_total_discount_item_price(self):
    #     return self.quantity * self.item.discount_price

    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        return self.get_total_item_price()

    
                
    def is_oreded(self):
            return self.ordered

   

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(CartItem)
    # start_date = models.DateTimeField(auto_now_add=True)
    # ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    # shipping_address = models.ForeignKey(
    #     'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    # billing_address = models.ForeignKey(
    #     'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey(
    #     'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    # being_delivered = models.BooleanField(default=False)
    # received = models.BooleanField(default=False)
    # refund_requested = models.BooleanField(default=False)
    # refund_granted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

        def is_oreded(self):
            return self.ordered
        def is_item(self):
            return self.items

    def get_total(self):
        total = 0
        for tom in self.items.all():
            total += tom.get_final_price()
        return total