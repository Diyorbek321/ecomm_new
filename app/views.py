from zipfile import error

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, ListView
from app.models import Category, Product, ProductImage, CategoryImage
from app.forms import CategoryForm, ProductForm, ProductImageForm, CategoryImageForm
import logging


# logger = logging.getLogger(__name__)


# Create your views here.
class UserDashboard(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'ecomm/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class CategoryView(TemplateView):
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
            context['image_form'] = CategoryImageForm(self.request.POST, self.request.FILES)
        else:
            # Check if the category has an existing primary image
            category = self.get_object()
            existing_image = CategoryImage.objects.filter(category=category, is_primary=True).first()
            context['image_form'] = CategoryImageForm(instance=existing_image)
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
            existing_image = CategoryImage.objects.filter(category=self.object, is_primary=True).first()

            if existing_image:
                # Update existing image
                existing_image.image = self.request.FILES['image']
                existing_image.save()
            else:
                # Create new image
                category_image = CategoryImage(
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
        context['image_form'] = ProductImageForm()
        context['products'] = Product.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        product_form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)

        if product_form.is_valid():
            # Save product
            product = product_form.save()

            # Handle single image upload
            if 'image' in request.FILES:
                ProductImage.objects.create(
                    product=product,
                    image=request.FILES['image'],
                    is_primary=True
                )

            messages.success(request, 'Product successfully added!')
            return redirect('admin-product')
        else:
            messages.error(request, 'Error adding product. Please check the form.')

        # If forms are invalid, render the page again
        context = self.get_context_data()
        context['product_form'] = product_form
        context['image_form'] = image_form
        return render(request, self.template_name, context)


class AdminReview(TemplateView):
    template_name = 'ecomm/admin/reviews.html'


class AdminUser(TemplateView):
    template_name = 'ecomm/admin/usermanagement.html'


class AdminPromotions(TemplateView):
    template_name = 'ecomm/admin/Promotions.html'
