from django.urls import path
from .views import RegisterView, LoginView, LogoutView, BeSellerView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="Register"),
    path('login/', LoginView.as_view(), name="Login"),
    path('logout/', LogoutView.as_view(), name="Logout"),
    path('be-seller/', BeSellerView.as_view(), name="BeSeller"),
]
