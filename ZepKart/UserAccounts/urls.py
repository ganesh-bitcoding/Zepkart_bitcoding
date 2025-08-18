from django.urls import path
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="Register"),
    path('login/', LoginView.as_view(), name="Login"),
    path('logout/', LogoutView.as_view(), name="Logout"),
]
