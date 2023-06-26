from django.db import models
from account.models import CustomUser

class Frige(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255) #영문숫자
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Drink(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255) # mysql에서 한글로 바꿔줘야함
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    frige = models.ForeignKey(Frige, on_delete=models.CASCADE, related_name='drinks')
    quantity = models.PositiveIntegerField(default=0)

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    frigename = models.CharField(max_length=255) 
    drinkname = models.CharField(max_length=255) # mysql에서 한글로 바꿔줘야함
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


# class FrigeItem(models.Model):
#     frige = models.ForeignKey(Frige, on_delete=models.CASCADE, related_name='items')
#     drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=0)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
