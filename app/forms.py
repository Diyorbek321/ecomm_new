from django import forms
from app.models import Category, Product, ProductImage, CategoryImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'slug', 'parent', 'status', 'description',
             'meta_title', 'meta_description', 'meta_keywords'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'id': 'slug'}),
            'parent': forms.Select(attrs={'class': 'form-select', 'id': 'parent'}),
            'status': forms.Select(attrs={'class': 'form-select', 'id': 'status'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'description', 'rows': '3'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control', 'id': 'meta_title'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'id': 'meta_description', 'rows': '2'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control', 'id': 'meta_keywords'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.all()
        self.fields['name'].required = True



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'sku', 'category', 'price', 'discount_price',
            'description', 'inventory', 'weight', 'status', 'tags',
            'seo_title', 'seo_description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter product description'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Type tags separated by commas'}),
            'seo_description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'SEO Meta Description'}),
        }


class CategoryImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'd-none',
            'id': 'image',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = CategoryImage
        fields = ['image']

class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = ProductImage
        fields = ['image']
