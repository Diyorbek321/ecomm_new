from django.urls import path
from app.views import UserDashboard, Category, Contact, ProductDetail, Cart, Checkout, About, Useraccount, Wishlist, \
        Autheticate, OrderConfirmation, AdminDashboard, AdminCategory, AdminOrder, AdminProduct, AdminPromotions, \
        AdminUser

urlpatterns = [
        path('',UserDashboard.as_view(),name='user_dashboard'),
        path('category/',Category.as_view(),name='category'),
        path('contact/',Contact.as_view(),name='contact'),
        path('product-detail/',ProductDetail.as_view(),name='product_detail'),
        path('product-cart/',Cart.as_view(),name='product_cart'),
        path('product-checkout/',Checkout.as_view(),name='product_checkout'),
        path('about/',About.as_view(),name='about'),
        path('user-account/',Useraccount.as_view(),name='user_account'),
        path('wishlist/',Wishlist.as_view(),name='wishlist'),
        path('authenticate/',Autheticate.as_view(),name='autheticate'),
        path('order-confirmation/',OrderConfirmation.as_view(),name='order'),



        path('admin-home/',AdminDashboard.as_view(),name='admin-home'),
        path('admin-category/',AdminCategory.as_view(),name='admin-category'),
        path('admin-product/',AdminProduct.as_view(),name='admin-product'),
        path('admin-promotions/',AdminPromotions.as_view(),name='admin-promotions'),
        path('admin-order/',AdminOrder.as_view(),name='admin-order'),
        path('admin-user/',AdminUser.as_view(),name='admin-user'),

]
