from django.db import models

# Create your models here.
LEVEL_CHOICES = [(x,str(x)) for x in range(1,6)]



class StoreList(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
    


class AddressList(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    category = models.ForeignKey(StoreList,on_delete=models.SET_DEFAULT,default=1)
    year = models.IntegerField()
    level = models.IntegerField(choices=LEVEL_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name



class QuakeList(models.Model):
    event_id = models.IntegerField()
    name = models.CharField(max_length=100)
    magnitude = models.FloatField()
    date = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return str(self.event_id)



class QuakeDetail(models.Model):
    event_id = models.ForeignKey(QuakeList,on_delete=models.CASCADE)
    prefecture = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    intensity = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.city
    


class CityList(models.Model):
    city_code = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100) 
    prefecture_code = models.CharField(max_length=100)
    prefecture_name = models.CharField(max_length=100)

    def __str__(self):
        return self.city_name