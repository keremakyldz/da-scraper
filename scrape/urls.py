from django.urls import path
from . import views

urlpatterns = [
    path("",views.brand, name="scrape"),
    path("<int:brand_id>/", views.detail, name="brand"),
    path('scrape/', views.scrape_and_show, name='scrape_and_show'),
]