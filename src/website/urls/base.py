from django.urls import path
from src.website import views

urlpatterns = [path("", views.HomePageView.as_view(), name="homepage")]
