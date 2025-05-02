from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, BlogPost, Category


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

class BlogPostForm(forms.ModelForm):
    new_category = forms.CharField(
        required=False,
        label="Or Create New Category",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a new category if needed'})
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'description', 'category', 'new_category', 'author', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your blog here...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False  