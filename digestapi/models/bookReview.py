from django.db import models
from django.contrib.auth.models import User


class BookReview(models.Model):

    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='book_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.CharField(max_length=155)
    date = models.DateField()