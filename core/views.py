from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg
from taggit.models import Tag

from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, WishList, ProductReview, Address
from core.forms import ProductReviewForm

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

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products_vendor = Product.objects.filter(product_status="published", vendor=product.vendor)
    
    #productr = get_object_or_404(Product, pid=pid) same with "Product.objects.get(pid=pid)"
    products_categories = Product.objects.filter(category=product.category).exclude(pid=pid)[:12]

    vendor_categories = Category.objects.filter(category__in=products_vendor).distinct()

    # Product Review form
    review_form = ProductReviewForm() 
    p_image = product.p_images.all() #Get all product images, p_image = ProductImages related name

    #Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    #Getting average reviews
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user__username=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    context = {
        "p": product,
        "make_review": make_review,
        "review_form": review_form,
        "p_image": p_image,
        "vendor_categories": vendor_categories,
        "related_products": products_categories,
        "reviews": reviews,
        "average_rating": average_rating,
    }

    return render(request, 'core/product-detail.html', context)

def tag_list(request, tag_slug=None):
    product = Product.objects.filter(product_status="published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = product.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag,
    }

    return render (request, "core/tag.html", context)

def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        "user": user.username,
        "review": request.POST['review'],
        "rating": request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse({
        "bool": True,
        "context": context,
        "average_reviews": average_reviews
    })
