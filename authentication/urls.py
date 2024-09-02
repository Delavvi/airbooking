from django.urls import path
from .views import MyLogInView, RegisterView, activate_account, EmailView, home

app_name = "authentication"

urlpatterns = [
    path("sign/", MyLogInView.as_view(), name='sign'),
    path("register/", RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate'),
    path("confirm-email/", EmailView.as_view(), name='email'),
    ]
