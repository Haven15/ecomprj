from django.urls import path
from core.views import index, product_filter_view, category_list_view, product_category_list_view, vendor_list_view, vendor_detail_view, product_detail_view

app_name = "core"

#indicate the url patterns
urlpatterns = [
    path("", index, name="index"),

    #Product
    path("products/", product_filter_view, name="product-filter"),
    path("product/<pid>", product_detail_view, name="product-detail"),

    #Category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>", product_category_list_view, name="product-category-list"),

    #Vendor
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>", vendor_detail_view, name="vendor-detail"),
]