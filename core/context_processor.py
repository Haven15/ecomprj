import logging
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, WishList, ProductReview, Address

logger = logging.getLogger(__name__)

def default(request):
    categories = Category.objects.all()
    
    address = None

    if request.user.is_authenticated:
        try:
            address = Address.objects.get(user__username=request.user)
        except Address.DoesNotExist:
            logger.warning(f"No Address found for user: {request.user}")

    return {
        'categories': categories,
        'address': address,
    }