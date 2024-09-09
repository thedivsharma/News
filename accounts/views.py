import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import AuthorForm, ArticleForm, LoginForm, CustomUserCreationForm
from .models import Authors, Article
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings

def home(request):
    articles = Article.objects.all().order_by('-published_at')
    return render(request, "home.html", {'articles': articles})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {'form': form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {'form': form})

@login_required(login_url="login")
def logout(request):
    request.session.flush()
    auth_logout(request)
    return redirect("home")

def post(request):
    return render(request, "post.html")

@login_required(login_url='login')
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Author added successfully!")
            return redirect('create_article')
    else:
        form = AuthorForm()
    return render(request, 'post.html', {'form': form})

@login_required(login_url='login')
def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Article added successfully!")
            return redirect('articles')
        else:
            print(form.errors)
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})

@login_required(login_url='login')
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'read.html', {'article': article})

@login_required(login_url='login')
def read(request):
    articles = Article.objects.all().order_by('-published_at')
    return render(request, 'read.html', {'articles': articles})

@login_required(login_url='login')
def author_list(request):
    try:
        authors = Authors.objects.all()
        if authors.exists():
            print(authors)
        else:
            messages.success(request, "No author found")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        authors = None
    return render(request, 'list_author.html', {'authors': authors})

def list_article(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list_article.html', {'articles': page_obj.object_list, 'page_obj': page_obj})

@login_required(login_url='login')
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        article.delete()
    return redirect('articles')

@login_required(login_url='login')
def edit(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit.html', {'form': form, 'article': article})

@login_required(login_url='login')
def delete_author(request, pk):
    author = Authors.objects.get(pk=pk)
    if request.method == "POST":
        author.delete()
    return redirect('authors')


def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_password_reset_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            otp = generate_otp()
            try:
                subject = 'Password Reset Request'
                message = f'''
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            color: #333;
                            margin: 0;
                            padding: 0;
                            background-color: #f4f4f4;
                        }}
                        .container {{
                            width: 80%;
                            margin: 20px auto;
                            background-color: #fff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 0 10px rgba(0,0,0,0.1);
                        }}
                        h1 {{
                            color: #007bff;
                            font-size: 24px;
                            margin-bottom: 20px;
                        }}
                        p {{
                            font-size: 16px;
                            line-height: 1.5;
                            margin-bottom: 20px;
                        }}
                        .otp {{
                            font-size: 18px;
                            font-weight: bold;
                            color: #007bff;
                            margin: 20px 0;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Login Request</h1>
                        <p>We see that you have forgotten your password , please us the OTP here to log yourself in</p>
                        <p class="otp">Your OTP is: {otp}</p>
                        
                        <p>Thank you, <br> The Team</p>
                    </div>
                </body>
                </html>
                '''

                email_message = EmailMessage(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )
                email_message.content_subtype = "html"
                email_message.send(fail_silently=False)

                request.session['otp'] = otp
                request.session['otp_email'] = email
            except Exception as e:
                print(f"An error occurred: {e}")
                messages.error(request, f"An error occurred: {e}")
            return redirect('verify_otp')
        else:
            pass
    return render(request, 'forgot_password.html')

from django.contrib.auth.models import User

def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        email = request.session.get('otp_email')
        if otp and otp == request.session.get('otp'):
            try:
                user = User.objects.get(email=email)
                if user:
                    auth_login(request, user)
                    return redirect('home')  
                else:
                    messages.error(request, "No user associated with this email.")
            except User.DoesNotExist:
                messages.error(request, "No user associated with this email.")
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, 'verify_otp.html')