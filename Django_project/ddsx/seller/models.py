from django.db import models

# Create your models here.

class Seller(models.Model):
	username = models.CharField(max_length=32)
	password = models.CharField(max_length=32)
	email = models.EmailField()
	phone = models.CharField(max_length=32)
	gender = models.BooleanField(default=True)
	address = models.TextField()
	head_img = models.ImageField(upload_to='img', null=True)

class Store(models.Model):
	name = models.CharField(max_length=32)
	address = models.TextField()
	desc = models.TextField()
	logo = models.ImageField(upload_to='img')
	# 一个卖家一个店铺
	seller = models.OneToOneField(to=Seller, on_delete=models.CASCADE)

class Goods_Type(models.Model):
	name = models.CharField(max_length=32)
	logo = models.ImageField(upload_to='img')
	seller = models.ForeignKey(to=Seller, on_delete=models.CASCADE, null=True)

class Goods(models.Model):
	name = models.CharField(max_length=32)
	price = models.FloatField()
	shelf_life = models.IntegerField()
	product_dt = models.DateField(null=True)
	desc = models.TextField()
	logo = models.ImageField(upload_to='img')
	content = models.TextField()

	goodstype = models.ForeignKey(to=Goods_Type, on_delete=models.CASCADE)
	store = models.ForeignKey(to=Store, on_delete=models.CASCADE, null=True, blank=True)




