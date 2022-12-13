from django.db import models
from django.contrib.auth.models import User
from apps.business_app.models import business
# Create your models here.

class userassociation(models.Model):
    user_reltn = models.ForeignKey(User, on_delete=models.CASCADE)
    business_reltn = models.ForeignKey(business, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_reltn.first_name}{self.user_reltn.last_name}'