# cd..
# jerryEnv\Scripts\activate
# cd clothing_store
# manage.py runserver

from locale import currency
from os import times
from django.db.models.fields import DecimalField
from django.http import request
from django.shortcuts import render, redirect, HttpResponse
from store_app.models import User, Product, ShippingOrder, BigBanner, SmallBanner, Order, OrderItem, UserOrder
from django.contrib import messages
import locale  # this formats to the local currency
from django.contrib import messages
import bcrypt
import json
import stripe
stripe.api_key = "sk_test_51HY4gxEB2brwFD1TquBo00MWvbpfPRP4KayLt0MGMkqBK4TfQnXnkCEGgXoz7rYbDGOzJ5q9PsTw6UxpMui9Xkty00ieOY3KZw"


# PAGES

def dash(request):  # DONE
    # request.session['userid'] = None
    if "cartnum" not in request.session:
        request.session["cartnum"] = 0

    if "tempNum" not in request.session:
        # get rid of this when finished this is a temp var
        request.session["tempNum"] = ""

    if "orderID" not in request.session:
        request.session["orderID"] = 0

    if "currentShipInfo" not in request.session:
        request.session['currentShipInfo'] = 0

    if "userid" not in request.session:
        request.session['userid'] = None

    if request.session['userid']:
        context = {
            "prods": Product.objects.all(),
            "bigBanner": BigBanner.objects.all(),
            "smallBanner": SmallBanner.objects.all(),
            "user": User.objects.get(id=request.session['userid']),
            "newFour": Product.objects.filter().order_by('-id')[:4]
        }
    else:
        context = {
            "prods": Product.objects.all(),
            "bigBanner": BigBanner.objects.all(),
            "smallBanner": SmallBanner.objects.all(),
            "newFour": Product.objects.filter().order_by('-id')[:4]
        }
    return render(request, 'dashboard.html', context)


def loginPage(request):
    return render(request, 'login.html')


def regPage(request):
    return render(request, 'reg.html')


def account(request, user_id):
    if request.session['userid']:
        user = User.objects.get(id=user_id)
        orderList = UserOrder.objects.all().filter(user=user)
        lastAddy = ShippingOrder.objects.filter(email=user.email).last()
        context ={
            "orderList": orderList,
            "lastAddy": lastAddy,
            "user": User.objects.get(id=request.session['userid'])
        }
        return render(request, 'account.html', context)
    else:
        return redirect('/account/login')


def orderInfo(request, order_id):
    if request.session['userid']:
        user = User.objects.get(id=request.session['userid'])
        order = Order.objects.get(id=order_id)
        context ={
            "order": order,
            "user": user,
            "addy": ShippingOrder.objects.filter(order=order).get(),
            "orderItems": OrderItem.objects.all().filter(order=order)
        }
        return render(request, 'orderInfo.html', context)
    else:
        return redirect('/account/login')


def infoPage(request, cat, prod_id):
    if request.session['userid']:
        context = {
            "prod": Product.objects.get(id=prod_id),
            "cat": cat,
            "user": User.objects.get(id=request.session['userid']),
        }
    else:
        context = {
            "prod": Product.objects.get(id=prod_id),
            "cat": cat
        }
    return render(request, 'info.html', context)


def category(request, gen, cat):
    if request.session['userid']:
        context = {
            "prods": Product.objects.all().filter(category=cat, gender=gen),
            "both": Product.objects.all().filter(category=cat, gender="B"),
            "user": User.objects.get(id=request.session['userid']),
        }
    else:
        context = {
            "prods": Product.objects.all().filter(category=cat, gender=gen),
            "both": Product.objects.all().filter(category=cat, gender="B")
        }
    return render(request, 'categoryPage.html', context)


# login

def reg(request):
    errors = SmallBanner.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/account/reg')
    else:
        password = request.POST['pass']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            email=request.POST['email'],
            password=pw_hash)
    return redirect('/account/login')


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if request.POST['next'] == "":
        nexturl = "/"
    else:
        nexturl = request.POST['next']
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['pass'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect(f'{nexturl}')
            # return redirect("/")
    else:
        messages.error(request, "Incorrect email or password.")
    return redirect('/account/login')


def logout(request):
    request.session['userid'] = None
    # messages.error(request, "You have successfully logged out")
    return redirect('/')


def logout2(request):
    request.session['userid'] = None
    # messages.error(request, "You have successfully logged out")
    return redirect('/checkout')


# CART
def cart(request):
    if request.session['cartnum'] == 0:
        return redirect('/')
    else:
        sesh_order = Order.objects.get(id=request.session["orderID"])
        cart_Items = OrderItem.objects.filter(order=sesh_order)

        locale.setlocale(locale.LC_ALL, '')  # <--money format
        cart_price = locale.currency(sesh_order.price)  # <--money format

        if request.session['userid']:
            context = {
                "cartItems": cart_Items,
                "cartPrice": cart_price,
                "user": User.objects.get(id=request.session['userid']),
            }
        else:
            context = {
                "cartItems": cart_Items,
                "cartPrice": cart_price,
            }
    return render(request, 'cart.html', context)


def addtocart(request, prod_id):
    prod = Product.objects.get(id=prod_id)
    if request.session["cartnum"] == 0:
        order = Order.objects.create(
            price=0.00,
        )
        request.session["orderID"] = order.id
        item = OrderItem.objects.create(
            product=prod,
            size=request.POST['size'],
            quantity=request.POST['qty'],
            order=order
        )
        itemPrice = item.product.price
        itemQty = item.quantity
        price = float(itemPrice) * float(itemQty)
        order.price = price
        order.save()
        # adds to cart number
        request.session["cartnum"] = request.session["cartnum"] + 1
    else:
        order = Order.objects.get(id=request.session["orderID"])
        item = OrderItem.objects.create(
            product=prod,
            size=request.POST['size'],
            quantity=request.POST['qty'],
            order=order
        )
        itemPrice = item.product.price
        itemQty = item.quantity
        price = float(itemPrice) * float(itemQty)
        newPrice = float(order.price) + float(price)
        order.price = newPrice
        order.save()
        request.session["cartnum"] = request.session["cartnum"] + 1
    return redirect('/')


def removeCartItem(request, item_id):
    order = Order.objects.get(id=request.session["orderID"])
    item = OrderItem.objects.get(id=item_id)

    itemPrice = item.product.price
    itemQty = item.quantity
    price = float(itemPrice) * float(itemQty)
    newPrice = float(order.price) - float(price)
    order.price = newPrice
    order.save()

    item.delete()
    request.session["cartnum"] = request.session["cartnum"] - 1

    return redirect('/cart')


def qtyUpCart(request, item_id):
    request.session["tempNum"] = item_id

    order = Order.objects.get(id=request.session["orderID"])
    item = OrderItem.objects.get(id=item_id)
    newQty = item.quantity + 1

    num_to_del = float(item.product.price) * float(item.quantity)
    order.price = float(order.price) - num_to_del
    item.quantity = newQty
    item.save()

    newItem = OrderItem.objects.get(id=item_id)
    price = float(newItem.product.price) * float(newItem.quantity)
    newPrice = float(order.price) + float(price)
    order.price = newPrice
    order.save()

    return redirect('/cart')


def qtyDownCart(request, item_id):
    request.session["tempNum"] = item_id

    order = Order.objects.get(id=request.session["orderID"])
    item = OrderItem.objects.get(id=item_id)
    newQty = item.quantity - 1

    num_to_del = float(item.product.price) * float(item.quantity)
    order.price = float(order.price) - num_to_del
    if newQty == 0:
        newQty = newQty + 1
        item.quantity = newQty
        item.save()
    else:
        item.quantity = newQty
        item.save()

    newItem = OrderItem.objects.get(id=item_id)
    price = float(newItem.product.price) * float(newItem.quantity)
    newPrice = float(order.price) + float(price)
    order.price = newPrice
    order.save()

    return redirect('/cart')


def checkout(request):
    if request.session['cartnum'] == 0:
        return redirect('/')
    else:
        sesh_order = Order.objects.get(id=request.session["orderID"])
        cart_Items = OrderItem.objects.filter(order=sesh_order)
        locale.setlocale(locale.LC_ALL, '')  # <--money format
        cart_price = locale.currency(sesh_order.price)  # <--money format
        if request.session['userid']:
            context = {
                "cartItems": cart_Items,
                "cartPrice": cart_price,
                "user": User.objects.get(id=request.session['userid']),
            }
        else:
            context = {
                "cartItems": cart_Items,
                "cartPrice": cart_price,
            }
    return render(request, 'checkout.html', context)




def thankyou(request):
    return render(request, 'thankYou.html')

# stripe


def charge(request):
    order = Order.objects.get(id=request.session["orderID"])
    first = request.POST['fname']
    last = request.POST['lname']
    
    errors = SmallBanner.objects.checkout_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/checkout')
    else:
        ShippingOrder.objects.create(
            email=request.POST['email'],
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            addy=request.POST['addy'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip_code=request.POST['zip_code'],
            order = order
        )
        if request.session['userid']:
            UserOrder.objects.create(
                user = User.objects.get(id=request.session['userid']),
                order = order,
            )
    #stripe
        chargeAmount = order.price * 100
        if request.method == 'POST':
            print('Data:', request.POST)

            customer = stripe.Customer.create(
                email=request.POST['email'],
                name=f"{first} {last}",
                source=request.POST['stripeToken']
            )
            charge = stripe.Charge.create(
                customer=customer,
                amount=int(chargeAmount),
                currency='usd',
                description="test charge"
            )
        request.session["cartnum"] = 0
        request.session["orderID"] = 0
        return redirect('/thankyou')