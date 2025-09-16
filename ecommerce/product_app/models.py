from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
class Item(models.Model):
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    category = models.ForeignKey(Category, related_name='cats',
    on_delete=models.CASCADE)
    def __str__(self):
        return self.name