from django.urls import path
from core.views import index, product_filter_view, category_list_view

app_name = "core"

#indicate the url patterns
urlpatterns = [
    path("", index, name="index"),
    path("products/", product_filter_view, name="product-filter"),
    path("category/", category_list_view, name="category-list")
]