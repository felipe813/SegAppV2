from django.test import TestCase
from django.test import Client
from accounts.forms import SignUpForm
from accounts.views import Views
from controller.viewsController import ViewsController
# Create your tests here.
class TestForms(TestCase):
    def test_sign_up(self):
        form = SignUpForm()
        self.assertTrue(isinstance(form,SignUpForm),"No es un ejemplar de la clase SignUpForm")
        self.assertTrue(form.fields != None,"El campo está vacío")

class TestViews(TestCase):
    def test_signup_with_post(self):
        views = Views()
        self.assertTrue(isinstance(views,Views),"No es un ejemplar de la clase Views")
        c = Client()
        c.post('/login/', {'name': 'fred', 'passwd': 'secret'})
        ctx = views.signup_with_post(c)
        self.assertTrue(ctx['form'] != None, "El contexto no se pudo obtener")

class TestViewsController(TestCase):
    def test_redirect(self):
        views_controller = ViewsController()
        self.assertTrue(isinstance(viewsController,ViewsController),"No es un ejemplar de la clase ViewsController")
        c = Client()
        c.get('/login/')
        viewsController.login(c)
