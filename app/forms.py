from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from app.models import Category, Product

User = get_user_model()


class LoginForm(AuthenticationForm):
    """Custom login form using email instead of username."""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'loginEmail',
            'placeholder': 'Email Address'
        }),
        label="Email"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'loginPassword',
            'placeholder': 'Password'
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'rememberMe'
        })
    )


class RegisterForm(UserCreationForm):
    """Custom registration form with additional fields."""
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'firstName',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'lastName',
            'placeholder': 'Last Name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'registerEmail',
            'placeholder': 'Email Address'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'registerPassword',
            'placeholder': 'Password'
        }),
        label="Password"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'confirmPassword',
            'placeholder': 'Confirm Password'
        }),
        label="Confirm Password"
    )

    agreed_to_terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'termsAgree'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'agreed_to_terms')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'slug', 'parent', 'status', 'description',
            'meta_title', 'meta_description', 'meta_keywords', 'image'
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
            'image': forms.FileInput(attrs={'class': 'form-control'}),
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
            'seo_title', 'seo_description', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter product description'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Type tags separated by commas'}),
            'seo_description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'SEO Meta Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
