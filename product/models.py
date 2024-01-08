from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from category.models import Category

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField(validators=[MinValueValidator(0),])
    quantity = models.IntegerField(validators=[MinValueValidator(0),])
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    contact_number = models.CharField(max_length=60, blank=True, null=True, verbose_name='Номер контакта автора')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        related_name='products',
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )



