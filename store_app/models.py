from django.db import models
from datetime import datetime

# Create your models here.
from django.db import models
from django.contrib.auth.models import UserManager
import re

from django.db.models.enums import Choices	# the regex module

# Create your models here.
class ShowManager(models.Manager):
    def login_validator(self, post_data):
        errors ={}
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        
        if len(post_data['fname']) < 2:
            errors['fname'] = "First Name must be at least 2 characters"

        if len(post_data['lname']) < 2:
            errors['lname'] = "Last Name must be at least 2 characters"

        if len(post_data['pass']) < 5:
            errors['pass'] = "Password has to be a minimum of 5 characters"

        return errors

    def checkout_validator(self, post_data):
        errors ={}
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        
        if len(post_data['fname']) < 2:
            errors['fname'] = "First Name must be at least 2 characters"

        if len(post_data['lname']) < 2:
            errors['lname'] = "Last Name must be at least 2 characters" 

        if len(post_data['addy']) < 1:
            errors['addy'] = "Address is Required"

        if len(post_data['city']) < 1:
            errors['city'] = "City is Required"

        if len(post_data['state']) < 1:
            errors['state'] = "State is Required"

        if len(post_data['zip_code']) < 5:
            errors['zip_code'] = "Invalid Zip!"

        return errors

    def payment_validator(self, post_data):
        errors ={}
        
        if len(post_data['ccName']) < 1:
            errors['ccName'] = "Card Name is Required"

        if len(post_data['ccNum']) < 16:
            errors['ccNum'] = "Invalid Card Number" 

        if len(post_data['ccCode']) < 3:
            errors['ccCode'] = "Invalid Security Code"

        if len(post_data['expdate']) < 1:
            errors['expdate'] = "Card Date is Required"

        if len(post_data['fname']) < 1:
            errors['fname'] = "First Name is Required"

        if len(post_data['lname']) < 1:
            errors['lname'] = "Last Name is Required" 

        if len(post_data['addy']) < 1:
            errors['addy'] = "Address is Required"

        if len(post_data['city']) < 1:
            errors['city'] = "City is Required"

        if len(post_data['state']) < 1:
            errors['state'] = "State is Required"

        if len(post_data['zip_code']) < 5:
            errors['zip_code'] = "Invalid Zip!"

        return errors



class User(models.Model): #customers
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    password = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model): #shirts, hats, boards...
    image = models.ImageField(null=False, default='default.jpg', upload_to='product_pics') #FOR MEDIA- /setting.py/urls.py
    name = models.CharField(max_length=50)

    def __str__(self): #this is to display a name for the admin side of this model
        return f'{self.name}' # to change the display name in django admin

    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    discount_price = models.DecimalField(max_digits=6, decimal_places=2,blank=True, null=True)

    categorieChoices = (
        ('S','shirt'),
        ('J','jacket'),
        ('H','hat'),
        ('SK','skateboard')
    )
    genderChoices = (
        ('B','both'),
        ('M','men'),
        ('W','woman'),
    )

    category = models.CharField(max_length=50, default="S", choices=categorieChoices)
    gender = models.CharField(max_length=20, default="B", choices=genderChoices)
    desc = models.TextField(max_length=200)
    oneSize = models.BooleanField(default=False)
    OSFA = models.IntegerField(default=0)
    S = models.IntegerField(default=0)
    M = models.IntegerField(default=0)
    L = models.IntegerField(default=0)
    XL = models.IntegerField(default=0)
    XXL = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    date = models.DateField(blank=True, default=datetime.now)
    Status = models.CharField(max_length=50, default="Processing Order")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserOrder(models.Model):
    user = models.ForeignKey(User, related_name="userOrders", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="userOrders", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model): 
    product = models.ForeignKey(Product, related_name="orderItems", on_delete = models.CASCADE)
    size = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, default=1, null=True, related_name="orderItems", on_delete = models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
class ShippingOrder(models.Model):
    email = models.EmailField(max_length=50) 
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    addy = models.CharField(max_length=50)
    addy2 = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)
    order = models.ForeignKey(Order, default=1, null=True, related_name="shippingOrder", on_delete = models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Name(models.Model):
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

class BigBanner(models.Model): 
    image = models.ImageField(null=False, default='default.jpg', upload_to='product_pics')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SmallBanner(models.Model): 
    image = models.ImageField(null=False, default='default.jpg', upload_to='product_pics')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = ShowManager() 
