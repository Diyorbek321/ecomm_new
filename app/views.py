from zipfile import error

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, ListView
from app.models import Category
from app.forms import CategoryForm
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class UserDashboard(TemplateView):
    template_name = 'ecomm/index.html'


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

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(self.request, "Category updated successfully!")
        return response

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        return Category.objects.get(pk=self.kwargs['pk'])


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
