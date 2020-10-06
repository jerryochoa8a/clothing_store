from store_app.views import account
from django.urls import path
from . import views

urlpatterns = [
    #PAGES
    path('info/<cat>/<prod_id>', views.infoPage),
    path('category/<gen>/<cat>', views.category),
    path('account/login', views.loginPage),
    path('account/reg', views.regPage),
    path('userId', views.account),
    path('', views.dash),

    
    #login
    path('logout2', views.logout2),
    path('logout', views.logout),
    path('account/<user_id>', views.account),
    path('account/orderInfo/<order_id>', views.orderInfo),
    path('login', views.login),
    path('reg', views.reg),

    #CART
    path('removeCartItem/<item_id>', views.removeCartItem),
    path('qtyUp/<item_id>', views.qtyUpCart),
    path('qtyDown/<item_id>', views.qtyDownCart),
    path('addtocart/<prod_id>', views.addtocart),
    path('thankyou', views.thankyou),
    path('checkout', views.checkout),
    path('cart', views.cart),

    #STRIPE

    path('charge', views.charge),

]