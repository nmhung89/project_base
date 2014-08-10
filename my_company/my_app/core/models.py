# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.gis.db import models as gismodels
from my_company.my_app.core import from_enum_choice
from django.contrib.auth.models import User

class HouseType(object):
    (CHUNG_CU, NHA_NGUYEN_CAN, NHA_TRO) = range(3)
    choices = [(CHUNG_CU, u'Chung cư'),
               (NHA_NGUYEN_CAN, u'Nhà nguyên căn'),
               (NHA_TRO, u'Phòng trọ'),]

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
    (ORIGINAL, SMALL, MEDIUM, LARGE) = range(4)
    choices = [(ORIGINAL, 'ORIGINAL'),
               (SMALL, 'SMALL'),
               (MEDIUM, 'MEDIUM'),
               (LARGE, 'LARGE')]

class District(models.Model):
    Pre = models.CharField(max_length=20)
    Name = models.CharField(max_length=100)
    Order = models.IntegerField(default=0)
    Center = gismodels.PointField(null=True)
    objects = gismodels.GeoManager()

class Ward(models.Model):
    Pre = models.CharField(max_length=20)
    District = models.ForeignKey('District')
    Name = models.CharField(max_length=100)
    Center = gismodels.PointField(null=True)
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
    SourceRef = models.CharField(max_length=200, null=True)
    Broker = models.ForeignKey('Broker', null=True)
    Staff = models.ForeignKey('Staff', null=True)
    Highlight = models.CharField(max_length=200)
    
    CreatedUser = models.ForeignKey(User, null=True)
    CreatedTime = models.DateTimeField(auto_now_add=True)
    UpdatedTime = models.DateTimeField(auto_now=True)
    NumView = models.IntegerField(default=0)
    NumCall = models.IntegerField(default=0)
    #Description
    Size = models.FloatField(null=True)
    BedRooms = models.IntegerField(null=True)
    Toalets = models.IntegerField(null=True)
    Price = models.DecimalField(max_digits=15, decimal_places=0)
    ElectricityPrice = models.CharField(max_length=50, null=True)
    WaterPrice = models.CharField(max_length=50, null=True)
    
    HasFurniture = models.NullBooleanField(null=True)
    HasInternet = models.NullBooleanField(null=True)
    IsFreeTime = models.NullBooleanField(null=True)
    IsSeperateGate = models.NullBooleanField(null=True)
    
    HasBalcony = models.NullBooleanField(null=True)
    CanCook = models.NullBooleanField(null=True)
    HasTvCable = models.NullBooleanField(null=True)
    IsQuiet = models.NullBooleanField(null=True)
    HasPrivateToalet = models.NullBooleanField(null=True)
    HasAirCondition = models.NullBooleanField(null=True)
    
    Description = models.TextField(null=True)
    #Address
    Phone = models.CharField(max_length=100)
    Address = models.CharField(max_length=200)
    Ward = models.ForeignKey('Ward', null=True)
    District = models.ForeignKey('District', null=True)
    Coordinate = gismodels.PointField(null=True)
    objects = gismodels.GeoManager()
    
class HouseImage(models.Model):
    Type = models.SmallIntegerField(choices=from_enum_choice(ImageType))
    House = models.ForeignKey('House', related_name='images')
    Name = models.CharField(max_length=100)
    
class Message(models.Model):
    Content = models.TextField()
    CreatedTime = models.DateTimeField(auto_now_add=True)