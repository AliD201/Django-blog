from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator

# Create your models here.
# from datetime import datetime

class Deal(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open deal'),
        ('Lost', 'Deal lost'),
        ('Won', 'Deal won'),
 
    )

    title = models.CharField(max_length=120)
    description = models.TextField()
    # default = timezone.now,
    date_created = models.DateField(auto_now_add = True)
    last_update = models.DateTimeField()
    close_time = models.DateTimeField()
    won_time = models.DateTimeField()
    lost_time = models.DateTimeField()
    handler = models.ForeignKey(User, on_delete=models.CASCADE)
    price =  models.FloatField(validators=[MinValueValidator(0)],)
    currency = models.CharField(max_length=4, default = "$")
    status = models.CharField(max_length=20, default='Open', choices=STATUS_CHOICES, verbose_name= 'status')
    # add groups role identification way here. 

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('deal-detail',kwargs={'pk': self.pk})