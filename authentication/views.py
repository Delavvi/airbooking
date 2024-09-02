from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .forms import RegisterForm, SignForm
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from .models import MyUser
from .tasks import send_activation_email


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = MyUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse('home'))
    else:
        return HttpResponse('Invalid activation link!')


class RegisterView(CreateView):
    model = MyUser
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        obj = MyUser.objects.create_user(username=username, email=email)
        obj.set_password(password)
        obj.save()
        self.object = obj
        current_site = get_current_site(self.request)
        token = default_token_generator.make_token(obj)
        send_activation_email.apply_async(args=[username, email, token, current_site.domain, obj.pk])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('authentication:email')


class EmailView(TemplateView):
    template_name = 'mail.html'


class MyLogInView(LoginView):
    form_class = SignForm
    template_name = 'log-in.html'
    success_url = reverse_lazy('polls:home')


def home(requests):
    return HttpResponse({'worked': 'work'})