# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.gis.db import models as gismodels
from my_company.my_app.core import from_enum_choice
from django.contrib.auth.models import User

class HouseType(object):
    (CHUNG_CU, NHA_RIENG, NHA_MAT_PHO, NHA_TRO) = range(4)
    choices = [(CHUNG_CU, 'Chung cư'),
               (NHA_RIENG, 'Nhà riêng'),
               (NHA_MAT_PHO, 'Nhà mặt phố'),
               (NHA_TRO, 'Phòng trọ'),]

class HouseStatus(object):
    (CHUA_THUE, DA_THUE, KHACH_WEB_THUE) = range(3)
    choices = [(CHUA_THUE, 'CHUA_THUE'),
               (DA_THUE, 'DA_THUE'),
               (KHACH_WEB_THUE, 'KHACH_WEB_THUE')
               ]

class HouseSource(object):
    (WEB, BROKER, STAFF, OTHERS) = range(4)
    choices = [(WEB, 'WEB'),
               (BROKER, 'BROKER'),
               (STAFF, 'STAFF'),
               (OTHERS, 'OTHERS')]

#SMALL: 200 X 150, MEDIUM: 520 X 500, LARGE: 840 X 500 
class ImageType(object):
    (SMALL, MEDIUM, LARGE) = range(3)
    choices = [(SMALL, 'SMALL'),
               (MEDIUM, 'MEDIUM'),
               (LARGE, 'LARGE')]

class District(models.Model):
    Pre = models.CharField(max_length=20)
    Name = models.CharField(max_length=100)
    Order = models.IntegerField()
    Center = gismodels.PointField()
    objects = gismodels.GeoManager()

class Ward(models.Model):
    Pre = models.CharField(max_length=20)
    District = models.ForeignKey('District')
    Name = models.CharField(max_length=100)
    Center = gismodels.PointField()
    objects = gismodels.GeoManager()

class Broker(models.Model):
    Name = models.CharField(max_length=200)
    Address = models.CharField(max_length=200)
    Phone = models.CharField(max_length=50)

class Staff(models.Model):
    Name = models.CharField(max_length=200)
    Phone = models.CharField(max_length=50)

class House(models.Model):
    #Properties
    Type = models.SmallIntegerField(choices=from_enum_choice(HouseType))
    Status = models.SmallIntegerField(choices=from_enum_choice(HouseStatus), default=HouseStatus.CHUA_THUE)
    Source = models.SmallIntegerField(choices=from_enum_choice(HouseSource))
    SourceRef = models.CharField(max_length=200)
    Broker = models.ForeignKey('Broker', null=True)
    Staff = models.ForeignKey('Staff', null=True)
    
    CreatedUser = models.ForeignKey(User)
    CreatedTime = models.DateTimeField(auto_now_add=True)
    UpdatedTime = models.DateTimeField(auto_now=True)
    NumView = models.IntegerField(default=0)
    NumCall = models.IntegerField(default=0)
    #Description
    Size = models.FloatField()
    BedRooms = models.IntegerField()
    Price = models.DecimalField(max_digits=15, decimal_places=0)
    ElectricityPrice = models.DecimalField(max_digits=15, decimal_places=0)
    WaterPrice = models.DecimalField(max_digits=15, decimal_places=0)
    
    HasFurniture = models.BooleanField()
    HasInternet = models.BooleanField()
    IsFreeTime = models.BooleanField()
    IsSeperateGate = models.BooleanField()
    Description = models.TextField()
    #Address
    Phone = models.CharField(max_length=100)
    Address = models.CharField(max_length=200)
    Ward = models.ForeignKey('Ward')
    Coordinate = gismodels.PointField()
    objects = gismodels.GeoManager()
    
class HouseImages(models.Model):
    Type = models.SmallIntegerField(choices=from_enum_choice(ImageType))
    House = models.ForeignKey('House')
    Url = models.CharField(max_length=100)
    