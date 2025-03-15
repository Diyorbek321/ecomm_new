from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    # Status choices
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    # Basic Fields
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        help_text="Auto-generated from name if left blank"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories',
        help_text="Parent category, if any"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True, null=True)

    # Image
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        help_text="Recommended size: 200x200px, Max size: 2MB"
    )

    # SEO Fields
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Comma-separated keywords"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    # Status choices for inventory status
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('out_of_stock', 'Out of Stock'),
        ('draft', 'Draft'),
    )

    # Basic Fields
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Discounted price, if applicable"
    )
    description = models.TextField(blank=True, null=True)

    # Inventory and Physical Details
    inventory = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Weight in kilograms"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # Images (Multiple)
    # We'll use a separate model for multiple images
    # SEO Fields
    seo_meta_title = models.CharField(max_length=200, blank=True, null=True)
    seo_meta_description = models.TextField(blank=True, null=True)

    # Tags (stored as a comma-separated string for simplicity)
    tags = models.CharField(max_length=200, blank=True, null=True, help_text="Comma-separated tags")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        """Return the discount price if available, otherwise the regular price."""
        return self.discount_price if self.discount_price is not None else self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"
