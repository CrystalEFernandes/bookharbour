from django.db import models

class Author(models.Model):
    name=models.CharField(max_length=100)
    bio=models.TextField()
    birth_date=models.DateField()
    nationality=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='author_photos/', null=True, blank=True)
