from django.contrib import admin
from django.urls import path, include
from resturent import views


urlpatterns = [
    path('',views.IndexView.as_view(),name="indexview"),
    path('about',views.AboutView.as_view(),name="aboutview"),
    path('table-book',views.BookView.as_view(),name="bookview"),
    path('menu',views.MenuView.as_view(),name="menuview"),
    path('sign-in',views.SigninView.as_view(),name="signinview"),
    path('sign-up',views.SignupView.as_view(),name="signupview"),
    path('profile',views.AccountView.as_view(),name="accountview"),
    path('signupajax',views.SignUpajaxView.as_view(),name="signupajaxview"),
]
