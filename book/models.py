from django.db import models
from authors.models import Author
from django.contrib.auth.models import User

class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    genre=models.CharField(max_length=50)
    description=models.TextField()
    publication_date=models.DateField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    language=models.CharField(max_length=50)
    pages=models.PositiveIntegerField()
    publisher=models.CharField(max_length=100)
    avg_rating=models.DecimalField(max_digits=3, decimal_places=2)
    stock_quantity=models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)