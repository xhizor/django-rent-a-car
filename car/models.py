from django.db import models


class FuelType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'fuel_type'

    def __str__(self):
        return self.name


class Engine(models.Model):
    name = models.CharField(max_length=30)
    power = models.FloatField()
    consumation = models.FloatField()
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE, related_name='engines')

    class Meta:
        db_table = 'engine'

    def __str__(self):
        return f'{self.name} | {self.power} KS - {self.consumation} l '


class Model(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'model'

    def __str__(self):
        return self.name


class AditionalEquipment(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'aditional_equipment'

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=20)
    model_year = models.IntegerField()
    price_hourly = models.FloatField()
    available = models.BooleanField(default=True)
    rate = models.FloatField(default=0)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='cars')
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE, related_name='cars')
    additional_equipment = models.ManyToManyField(AditionalEquipment, related_name='cars')

    class Meta:
        db_table = 'car'

    def __str__(self):
        return f'{self.model.name} {self.name} | {self.engine.name} - {self.model_year} | ' \
               f'${self.price_hourly} - ' + 'Available' if self.available else 'Unavailable'


class Galery(models.Model):
    photo = models.ImageField(upload_to='cars/%Y/%m/%d')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='photos')

    class Meta:
        db_table = 'galery'

    def __str__(self):
        return self.car


