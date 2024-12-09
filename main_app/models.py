from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User, AbstractUser


# Create your models here.


class Garden(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    

    
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('garden-detail', kwargs={'pk': self.id})
    
class Plot(models.Model):
    name = models.CharField(max_length=100)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    days_since_watered = models.IntegerField(db_column='daysincewatered',default=0)

    def __str__(self):
        return self.name    

    def get_absolute_url(self):
        return reverse('plot-detail', kwargs={'plot_id': self.id})
    
    def increment_days(self):
        self.days_since_watered += 1
        self.save()
   

    

class Plant(models.Model):
    name=models.CharField(max_length=100)
    days_since_planted=models.IntegerField(db_column='days_since_planted',default=0)
    days_until_mature=models.IntegerField(db_column='days_until_mature')
    description=models.TextField(max_length=250)
    plot=models.ForeignKey(Plot, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plant-detail', kwargs={'pk': self.id,'plot_id': self.plot.id, 'garden_id': self.plot.garden.id})
