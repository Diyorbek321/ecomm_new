from zipfile import error

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, ListView, DetailView
from app.models import Category, Product
from app.forms import CategoryForm, ProductForm, LoginForm, RegisterForm
import logging


# logger = logging.getLogger(__name__)


# Create your views here.
class UserDashboard(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'ecomm/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the paginated products
        products = Product.objects.all()
        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context['products'] = page_obj
        context['is_paginated'] = True
        context['page_obj'] = page_obj

        return context


class CategoryView(ListView):
    model = Product
    template_name = 'ecomm/productlisting.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.request.GET.get('id')
        if category_id:
            return Product.objects.filter(category__id=category_id)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('id')
        if category_id:
            context['category'] = Category.objects.get(id=category_id)
        return context


class Contact(TemplateView):
    template_name = 'ecomm/contact.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'ecomm/productdetail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related products (same category)
        related_products = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]  # Limit to 4 related products
        context['related_products'] = related_products
        return context


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


class Authenticate(TemplateView):
    template_name = 'ecomm/authenticate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['register_form'] = RegisterForm()
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        if 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.username = user.email  # Use email as username
                user.save()
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('autheticate')
            else:
                login_form = LoginForm()
                return render(request, self.template_name, {
                    'login_form': login_form,
                    'register_form': register_form,
                    'active_form': 'register'
                })
        elif 'login' in request.POST:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data.get('username')  # This is email because we overrode the field
                password = login_form.cleaned_data.get('password')
                remember_me = login_form.cleaned_data.get('remember_me')

                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)  # Session expires when browser is closed
                    return redirect('user_dashboard')  # Change to your post-login page
                else:
                    messages.error(request, 'Invalid email or password')
            register_form = RegisterForm()
            return render(request, self.template_name, {
                'login_form': login_form,
                'register_form': register_form,
                'active_form': 'login'
            })

        # If we get here, something went wrong
        return self.get(request, *args, **kwargs)


class OrderConfirmation(TemplateView):
    template_name = 'ecomm/orderconfirmation.html'


class AdminDashboard(TemplateView):
    template_name = 'ecomm/admin/home.html'


class AdminCategory(ListView):
    model = Category
    template_name = 'ecomm/admin/category.html'
    context_object_name = 'categories'
    paginate_by = 7

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the form to the context for GET requests
        context['form'] = CategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "Category added successfully!")
            return self.get(request, *args, **kwargs)  # Reload the list page
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            messages.error(request, "Please correct the errors below.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class AdminCategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'ecomm/admin/category.html'
    success_url = reverse_lazy('admin-category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_form'] = CategoryForm(self.request.POST, self.request.FILES)
        else:
            # Check if the category has an existing primary image
            category = self.get_object()
            existing_image = Category.objects.filter(category=category, is_primary=True).first()
            context['image_form'] = Category(instance=existing_image)
            context['existing_image'] = existing_image
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = context['image_form']

        # Save the category first
        self.object = form.save()

        # Now handle the image form if it has data
        if 'image' in self.request.FILES:
            # Check if there's an existing primary image
            existing_image = Category.objects.filter(category=self.object, is_primary=True).first()

            if existing_image:
                # Update existing image
                existing_image.image = self.request.FILES['image']
                existing_image.save()
            else:
                # Create new image
                category_image = Category(
                    category=self.object,
                    image=self.request.FILES['image'],
                    is_primary=True
                )
                category_image.save()

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(self.request, "Category updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        return Category.objects.get(pk=self.kwargs['pk'])


class AdminOrder(TemplateView):
    template_name = 'ecomm/admin/ordermanagement.html'


class AdminProduct(ListView):
    template_name = 'ecomm/admin/productmanagement.html'
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = ProductForm()
        # Remove the image_form since we're no longer using it
        context['products'] = Product.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # Pass request.FILES to the ProductForm to handle the image upload
        product_form = ProductForm(request.POST, request.FILES)

        if product_form.is_valid():
            # Save product (image will be saved automatically as part of the form)
            product = product_form.save()
            messages.success(request, 'Product successfully added!')
            return redirect('admin-product')
        else:
            messages.error(request, 'Error adding product. Please check the form.')

        # If form is invalid, render the page again
        context = self.get_context_data()
        context['product_form'] = product_form
        return render(request, self.template_name, context)


class AdminReview(TemplateView):
    template_name = 'ecomm/admin/reviews.html'


class AdminUser(TemplateView):
    template_name = 'ecomm/admin/usermanagement.html'


class AdminPromotions(TemplateView):
    template_name = 'ecomm/admin/Promotions.html'
