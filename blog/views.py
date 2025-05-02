from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, BlogPostForm
from .models import BlogPost, Category

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/dashboard.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            # Check if new category is provided
            new_category_name = form.cleaned_data.get('new_category')
            
            # If new category is entered, create or get existing category
            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
                post.category = category  # Assign the category to the post

            # If no new category is entered, use the selected category from the dropdown
            else:
                post.category = form.cleaned_data.get('category')

            post.author = request.user
            post.save()
            return redirect('dashboard')  # Redirect to homepage or list page
    else:
        form = BlogPostForm()

    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
                post.category = category
            else:
                post.category = form.cleaned_data.get('category')
            form.save()
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    post.delete()
    return redirect('dashboard')

def home(request):
    posts = BlogPost.objects.all().order_by('-publish_date')
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


