from django import forms
from app.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'slug', 'parent', 'status', 'description',
            'image', 'meta_title', 'meta_description', 'meta_keywords'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'id': 'slug'}),
            'parent': forms.Select(attrs={'class': 'form-select', 'id': 'parent'}),
            'status': forms.Select(attrs={'class': 'form-select', 'id': 'status'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'description', 'rows': '3'}),
            'image': forms.FileInput(attrs={'class': 'd-none', 'id': 'image', 'accept': 'image/*'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control', 'id': 'meta_title'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'id': 'meta_description', 'rows': '2'}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control', 'id': 'meta_keywords'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.all()
        self.fields['name'].required = True

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 2 * 1024 * 1024:  # 2MB
            raise forms.ValidationError("Image file size must be less than 2MB.")
        return image