import logging
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, WishList, ProductReview, Address

logger = logging.getLogger(__name__)

def default(request):
    logger.warning(f'Request user: {request.user}')
    logger.warning(f'Is authenticated: {request.user.is_authenticated}')

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