from django.contrib.auth import login as auth_login

from .forms import SignUpForm

def signup_with_post(request):
    form = SignUpForm(request.POST)
    ctx = {'form': form}
    return ctx

def signup_no_post():
    form = SignUpForm()
    ctx = {'form': form}
    return ctx

def autenticar(request, form):
    user = form.save()
    auth_login(request, user)
