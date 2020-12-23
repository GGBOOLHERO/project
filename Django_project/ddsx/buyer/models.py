from django.db import models

# Create your models here.

class Buyer(models.Model):
	name = models.CharField(max_length=32)
	password = models.CharField(max_length=32)
	email = models.EmailField()
	phone = models.CharField(max_length=32)
	address = models.TextField()


class Car(models.Model):
	goods_id = models.IntegerField(default=1)
	store_id = models.IntegerField(default=1)
	goods_name = models.CharField(max_length=32)
	goods_img = models.CharField(max_length=32)
	goods_price = models.DecimalField(max_digits=5, decimal_places=2)
	goods_num = models.IntegerField(default=1)
	buyer = models.ForeignKey(to=Buyer, on_delete=models.CASCADE)

class BuyerAddress(models.Model):
	name = models.CharField(max_length=32)
	address = models.TextField()
	email = models.CharField(max_length=32)
	phone = models.CharField(max_length=32)
	status = models.BooleanField(default=False)
	buyer = models.ForeignKey(to=Buyer, on_delete=models.CASCADE)

class Order(models.Model):
	order_no = models.CharField(max_length=32)
	order_date = models.DateField()
	order_address = models.CharField(max_length=128)
	order_total_num = models.CharField(max_length=32)
	order_total_price = models.CharField(max_length=32, default=0)
	status = models.BooleanField(default=False)
	buyer = models.ForeignKey(to=Buyer, on_delete=models.CASCADE)

class OrderDetail(models.Model):
	goods_name = models.CharField(max_length=32)
	goods_price = models.DecimalField(max_digits=5, decimal_places=2)
	goods_num = models.IntegerField()
	goods_total_price = models.CharField(max_length=32)
	goods_img = models.CharField(max_length=32)
	order = models.ForeignKey(to=Order, on_delete=models.CASCADE)

class CheckEmail(models.Model):
	email = models.CharField(max_length=32)
	code = models.CharField(max_length=32)
	date = models.DateTimeField(max_length=32)

