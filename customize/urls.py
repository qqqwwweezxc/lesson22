from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('register/', views.register_view, name='register'),
    path("api/products/", views.ProductList.as_view()),
    path("api/products/<int:pk>/", views.ProductDetail.as_view()),
    path('expensive_products/', views.expensive_products),
]