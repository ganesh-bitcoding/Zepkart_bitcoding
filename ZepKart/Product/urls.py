from django.urls import path
from .views import AddProductView, SellerProductView,SellerProductUpdateView, SellerProductDeleteView, SellerProductDetailsView


urlpatterns = [
    path("add-product/", AddProductView.as_view(), name="AddProduct"),
    path("my-product/", SellerProductView.as_view(), name="myproductlist"),
    path("update-product/<str:pk>/", SellerProductUpdateView.as_view(), name="UpdateProduct"),
    path("delete-product/<str:pk>/", SellerProductDeleteView.as_view(), name="DeleteProduct"),
    path("detail-of-product/<str:pk>/", SellerProductDetailsView.as_view(), name="DetailedProduct"),
]
