from django.db import models
from django.contrib.auth.models import User

# Products Class
class Product(models.Model):
      
    title = models.CharField(max_length=250)
    url = models.CharField(max_length=300)
    pub_date = models.DateField(auto_now=True)
    votes_total = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    body = models.TextField(max_length=1000)
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')
    
    def __str__(self):
        return self.title
