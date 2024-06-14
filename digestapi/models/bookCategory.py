from django.db import models

class BookCategory(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='book_categories')
    category = models.ForeignKey('Category', on_delete=models.CASCADE,  related_name='book_categories')
    date = models.DateField()