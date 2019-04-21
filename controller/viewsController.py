from accounts import views as views_accounts
from mapa import views as views_mapa

from django.contrib.auth import views as auth_views

from django.shortcuts import render
#from django.shortcuts import render_to_response
from django.shortcuts import redirect

#from django.http import HttpResponse

def index(request):
    print("index")
    if(request.user.is_authenticated):
        ctx = {}
        return render(request,'index.html',ctx)
    else:
        return redirect('login')

def mapa(request):
    print("mapa")
    if(request.user.is_authenticated):
        ctx = views_mapa.mapa(request)
        return render(request,'mapa.html',ctx)
    else:
        return redirect('login')

def signup(request):
    print("signup")
    if request.method == 'POST':
        ctx = views_accounts.signupWithPost(request)
        form = ctx['form']
        if(form.is_valid()):
            views_accounts.autenticar(request, form)
            return home(request)
    else:
        ctx = views_accounts.signupNoPost()
    return render(request, 'signup.html', ctx)

def login(request):
    print("login")
    if request.user.is_authenticated:
        print("login : usuario autenticado")
        return index(request)
    else:
        print("login : usuario iniciará sesión")
        return auth_views.LoginView.as_view(template_name='login.html')(request)

def logout(request):
    print("logout")
    return auth_views.LogoutView.as_view()(request)

def home(request):
    print("home")
    if(request.user.is_authenticated):
        return index(request)
    else:
        return redirect('login')
