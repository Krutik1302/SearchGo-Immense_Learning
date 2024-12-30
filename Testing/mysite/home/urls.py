from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("login/", views.loginView.as_view(), name = 'login'),
    path("signup/", views.signup.as_view(), name = 'signup'),
    path("", views.homePage.as_view(), name = 'home'),
    path("about/", views.aboutpage.as_view(), name = 'about'),
    path("terms/", views.terms.as_view(), name = 'terms'),
    path("addlink/", views.addlink.as_view(), name = 'addlink'),
    path("logout/", views.LogoutView.as_view()),
    path("contactus/", views.contactus.as_view(), name = 'contactus'),
]