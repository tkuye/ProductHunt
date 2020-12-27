from django.core import serializers
from django.db import models
from django.contrib.auth.models import User
from django.db.models import fields

# Products Class
class Product(models.Model):
      
    title = models.CharField(max_length=250)
    url = models.CharField(max_length=300)
    pub_date = models.DateField(auto_now_add=True)
    votes_total = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    body = models.TextField()
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')
    
    def __str__(self):
        return self.title

class Vote(models.Model):
    productId = models.ForeignKey(Product,on_delete=models.CASCADE)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)


class Comment(models.Model):
    username = models.CharField(max_length=50)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    productId = models.ForeignKey(Product,on_delete=models.CASCADE)
    comment = models.TextField()









    
