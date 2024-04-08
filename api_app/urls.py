from django.urls import path
from .views import SignupView, RootView, UserDetailsView, LoginView, ReferralsView

urlpatterns = [
    path("", RootView.as_view()),
    path("signup", SignupView.as_view()),
    path("login", LoginView.as_view()),
    path("profile", UserDetailsView.as_view()),
    path("referrals", ReferralsView.as_view()),
]
