from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def register(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)

        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')

        # Create a new User object with the provided information
        user = User.objects.create_user(
            email=email,
            username=username
        )

        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/blog/')

    # Render the registration page template (GET request)
    return render(request, 'sign_in.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/home/')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def blog(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'posts': posts})


@login_required
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_detail.html', {'post': post})


@login_required
def editor(request):
    if request.method == 'POST':
        print("hello")
        form = BlogPostForm(request.POST)
        blog_post = form.save(commit=False)
        blog_post.author = request.user
        blog_post.save()
        return redirect('blog_detail', pk=blog_post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'editor.html', {'form': form})


@login_required
def blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            form.author = request.user
            form.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog_edit.html', {'form': form, 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('blog')
    return render(request, 'post_confirm_delete.html', {'post': post})
