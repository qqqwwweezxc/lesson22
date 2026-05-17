from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter

from .forms import RegisterForm
from .middleware import get_request_count
from .models import Product
from .permissions import CustomPermission
from .serializers import ProductSerializer


class ProductListView(ListView):
    """Renders a list of products"""
    model = Product
    template_name = "customize/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(quantity__gt=0).order_by("-price")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Available Products"
        context["total_products"] = self.get_queryset().count()

        return context

    
def register_view(request: HttpRequest) -> HttpResponse:
    """Renders the register page"""
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = RegisterForm()

    return render(request, "customize/register.html", {"form": form})


class ProductList(generics.ListCreateAPIView):
    """Renders a list of products"""
    queryset = Product.objects.prefetch_related("reviews")
    serializer_class = ProductSerializer
    permission_classes = [CustomPermission]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = ["price", "quantity"]

    search_fields = ["name"]

    ordering_fields = ["price", "quantity"]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """Renders a product detail"""
    queryset = Product.objects.prefetch_related("reviews")
    serializer_class = ProductSerializer
    permission_classes = [CustomPermission]


def expensive_products(request: HttpRequest) -> HttpResponse:
    """Renders a list of expensive products"""
    products = Product.objects.raw("""
        SELECT * 
        FROM customize_product
        WHERE price * quantity > 1000
    """)

    return render(request, "customize/products.html", {"products": products})


def stats_view(request: HttpRequest) -> HttpResponse:
    """Renders the stats page"""
    return JsonResponse({
        "requests_count": get_request_count()
    })