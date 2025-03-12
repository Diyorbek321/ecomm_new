from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class UserDashboard(TemplateView):
    template_name = 'ecomm/index.html'


class Category(TemplateView):
    template_name = 'ecomm/productlisting.html'


class Contact(TemplateView):
    template_name = 'ecomm/contact.html'


class ProductDetail(TemplateView):
    template_name = 'ecomm/productdetail.html'


class Cart(TemplateView):
    template_name = 'ecomm/cart.html'


class Checkout(TemplateView):
    template_name = 'ecomm/chekout.html'


class About(TemplateView):
    template_name = 'ecomm/aboutus.html'

class Useraccount(TemplateView):
    template_name = 'ecomm/useraccount.html'

class Wishlist(TemplateView):
    template_name = 'ecomm/wishlist.html'

class Autheticate(TemplateView):
    template_name = 'ecomm/authenticate.html'

class OrderConfirmation(TemplateView):
    template_name = 'ecomm/orderconfirmation.html'

class AdminDashboard(TemplateView):
    template_name = 'ecomm/admin/home.html'

class AdminCategory(TemplateView):
    template_name = 'ecomm/admin/category.html'

class AdminOrder(TemplateView):
    template_name = 'ecomm/admin/ordermanagement.html'

class AdminProduct(TemplateView):
    template_name = 'ecomm/admin/productmanagement.html'

class AdminReview(TemplateView):
    template_name = 'ecomm/admin/reviews.html'

class AdminUser(TemplateView):
    template_name = 'ecomm/admin/usermanagement.html'

class AdminPromotions(TemplateView):
    template_name = 'ecomm/admin/Promotions.html'