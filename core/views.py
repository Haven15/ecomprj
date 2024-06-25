from django.http import HttpResponse
from django.shortcuts import render

from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, WishList, ProductReview, Address


def index(request):
    #products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured=True)

    context = {
        "products": products
    }

    return render(request, 'core/index.html', context)

def product_filter_view(request):
    products = Product.objects.filter(product_status="published")

    context = {
        "products": products
    }

    return render(request, 'core/product-filter.html', context)

def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories": categories
    }

    return render(request, 'core/category-list.html', context)

def product_category_list_view(request, cid):
    category = Category.objects.get(cid=cid) #ex. Food Category
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category": category,
        "products": products
    }

    return render(request, 'core/product-category-list.html', context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {
        "vendors": vendors
    }

    return render(request, 'core/vendors-list.html', context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status="published", vendor=vendor)
    categories = Category.objects.all()
    vendor_categories = Category.objects.filter(category__in=products).distinct()

    context = {
        "vendor": vendor,
        "products": products,
        "categories": categories,
        "vendor_categories": vendor_categories
    }

    return render(request, 'core/vendor-details-2.html', context)
