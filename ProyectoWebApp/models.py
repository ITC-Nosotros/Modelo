from django.db import models

# Create your models here.
class CarSelection(models.Model):
    OPCIONES_CAR = [
        ('Mazda 2', 'Mazda 2'),
        ('Toyota Corolla', 'Toyota Corolla'),
        ('Suzuki Swift', 'Suzuki Swift'),
        ('Renault Duster', 'Renault Duster'),
        ('Chevrolet Onix', 'Chevrolet Onix'),
    ]
    car_choice = models.CharField(max_length=20, choices=OPCIONES_CAR)

    OPCIONES_LOCATIONS = [
        ('Antioquia', 'Antioquia'),
        ('Nariño', 'Nariño'),
        ('Valle Del Cauca', 'Valle Del Cauca'),
        ('Risaralda', 'Risaralda'),
        ('Boyaca', 'Boyaca'),
        ('Bogotá D.C.', 'Bogotá D.C.'),
        ('Cundinamarca', 'Cundinamarca'),
        ('Atlántico', 'Atlántico'),
        ('Caldas', 'Caldas'),
        ('Norte De Santander', 'Norte De Santander'),
        ('Santander', 'Santander'),
        ('Meta', 'Meta'),
        ('Cesar', 'Cesar'),
        ('Huila', 'Huila'),
        ('Tolima', 'Tolima'),
        ('Córdoba', 'Córdoba'),
        ('Bolívar', 'Bolívar'),
        ('Casanare', 'Casanare'),
        ('Quindio', 'Quindio'),
    ]
    location = models.CharField(max_length=50, choices=OPCIONES_LOCATIONS)

    price_range = models.PositiveIntegerField()
    km_range = models.PositiveIntegerField()
    yearmodel_range = models.PositiveIntegerField()
    
    