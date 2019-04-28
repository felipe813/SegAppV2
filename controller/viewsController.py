from accounts import views as views_accounts
from mapa import views as views_mapa

from django.contrib.auth import views as auth_views

from django.shortcuts import render
from django.shortcuts import redirect

class ViewsController():

    def __init__(self):
        self.__views_accounts = views_accounts.Views()
        self.__views_mapa = views_mapa.Views()

    def index(self, request):
        print("index")
        if(request.user.is_authenticated):
            ctx = {}
            return render(request,'index.html',ctx)
        else:
            return redirect('login')

    def mapa(self, request):
        print("mapa")
        if(request.user.is_authenticated):
            ctx = self.__views_mapa.mapa(request)
            return render(request,'mapa.html',ctx)
        else:
            return redirect('login')

    def signup(self, request):
        print("signup")
        if request.method == 'POST':
            ctx = self.__views_accounts.signup_with_post(request)
            form = ctx['form']
            if(form.is_valid()):
                self.__views_accounts.autenticar(request, form)
                return self.home(request)
            else:
                ctx = self.__views_accounts.signup_no_post()
            return render(request, 'signup.html', ctx)

    def login(self, request):
        print("login")
        if request.user.is_authenticated:
            print("login : usuario autenticado")
            return self.index(request)
        else:
            print("login : usuario iniciara sesion")
            return auth_views.LoginView.as_view(template_name='login.html')(request)

    def logout(self, request):
        print("logout")
        return auth_views.LogoutView.as_view()(request)

    def home(self, request):
        print("home")
        if(request.user.is_authenticated):
            return self.index(request)
        else:
            return redirect('login')
