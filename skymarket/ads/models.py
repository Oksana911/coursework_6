from django.db import models
from users.models import User


class Ad(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ad')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text
