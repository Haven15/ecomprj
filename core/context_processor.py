from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, WishList, ProductReview, Address


def default(request):
    categories = Category.objects.all()

    return {
        'categories': categories,
    }