from django.contrib.auth import login as auth_login

from .forms import SignUpForm
class Views():
    def signup_with_post(self, request):
        form = SignUpForm(request.POST)
        ctx = {'form': form}
        return ctx

    def signup_no_post(self):
        form = SignUpForm()
        ctx = {'form': form}
        return ctx

    def autenticar(self, request, form):
        user = form.save()
        auth_login(request, user)
