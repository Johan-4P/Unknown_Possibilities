from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name
    
class Product(models.Model):
    """Model representing a product."""
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)
    stock = models.IntegerField(default=0, null=True, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class TarotCard(models.Model):
    """A model for picking a tarot card."""
    name = models.CharField(max_length=100)
    image = CloudinaryField('image', blank=True, null=True)
    message = models.TextField()
    categories = models.ManyToManyField('Category', related_name='tarot_cards')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='cards', null=True, blank=True)

    def __str__(self):
        return self.name
