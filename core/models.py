from django.db import models
from shortuuid.django_fields import ShortUUIDField  #Short UUIDField for Django
from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered")
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published")
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★")
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}.format(instance.user.id, filename)'

class Category(models.Model):
    #Category ID
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345") #ex. cat1234567890
    title = models.CharField(max_length=100, default="Food") #Title, Heading
    image = models.ImageField(upload_to="category", default="category.jpg") #Image uploaded will be uploaded to category folder(automatically created)      

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")

    title = models.CharField(max_length=100, default="Nestify") #Title, Heading
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg") #Image uploaded will be uploaded to user directory path folder(automatically created)
    description = models.TextField(null=True, blank=True, default="I am an amazing Vendor")

    address = models.CharField(max_length=100, default="123 Main Street.")
    contact = models.CharField(max_length=100, default="+123 (456) 789")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    #Whenever a user is deleted, the shop or vendor of that user is also deleted
    #user = models.ForeignKey(User, on_delete=models.Cascade)

    #Whenever a user is deleted, the shop or vendor of that user will be changed to null
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    #Product ID
    pid  = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")

    #Whenever a user is deleted, the shop or vendor of that product will be changed to null
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100, default="Fresh Pear") #Title, Heading
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg") #Image uploaded will be uploaded to user directory path folder(automatically created)
    description = models.TextField(null=True, blank=True, default="This is the product")

    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99") #ex. 20.99
    old_price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="2.99") #ex. 20.99

    specifications = models.TextField(null=True, blank=True)
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    #Stock Keeping Units
    sku  = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        #Discounted price
        new_price = (1 - (self.price / self.old_price)) * 100
        return new_price

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

####################################################### Cart, Order and OrderItems #######################################################
####################################################### Cart, Order and OrderItems #######################################################
####################################################### Cart, Order and OrderItems #######################################################
####################################################### Cart, Order and OrderItems #######################################################

class CartOrder(models.Model):
    #If user is deleted, the cart is also deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99") #ex. 20.99
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99") #ex. 20.99
    total = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99") #ex. 20.99

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

####################################################### Product Review, wishlists, Address #######################################################
####################################################### Product Review, wishlists, Address #######################################################
####################################################### Product Review, wishlists, Address #######################################################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"
    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wishlists"
    
    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"
