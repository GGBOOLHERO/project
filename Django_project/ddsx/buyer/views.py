from django.shortcuts import render, HttpResponse, redirect
from buyer.models import *
from seller.models import *
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
import random


# Create your views here.

def register(request):
	if request.method == 'POST':
		username = request.POST.get('user_name')
		password = request.POST.get('user_pwd')
		email = request.POST.get('user_email')
		phone = request.POST.get('phone')
		address = request.POST.get('address')
		buyer_obj = Buyer()
		buyer_obj.name = username
		buyer_obj.password = password
		buyer_obj.email = email
		buyer_obj.phone = phone
		buyer_obj.address = address
		buyer_obj.save()
		return redirect('/buyer/login/')
	return render(request, 'buyer/register.html')

def login(request):
	if request.method == 'POST':
		username = request.POST.get('user_name')
		password = request.POST.get('user_pwd')
		buyer_obj = Buyer.objects.filter(name=username, password=password).first()
		if buyer_obj:
			response = redirect('/buyer/index/')
			response.set_cookie('buyer_id', buyer_obj.id)
			response.set_cookie('buyer_name', buyer_obj.name)
			return response
		else:
			msg = '账号或密码错误'
	return render(request, 'buyer/login.html', locals())

def logout(request):
	response = redirect('/buyer/login/')
	response.delete_cookie('seller_name')
	response.delete_cookie('seller_id')
	return response

def index(request):
	goodstype_obj_list = Goods_Type.objects.all()
	goods_obj_list = Goods.objects.all()
	lb_goods_obj_list = Goods.objects.all().order_by('-id')[0:4]
	return render(request, 'buyer/index.html', locals())

# def more_goods_list(request):
# 	goodstype_obj_id = request.GET.get('goodstype_id')
# 	goods_obj_list = Goods.objects.filter(goodstype_id=goodstype_obj_id)
# 	return render(request, 'buyer/list_test.html', locals())
#
# def more_goods_list(request):
# 	goodstype_obj_id = request.GET.get('goodstype_id')
# 	goods_obj_list = Goods.objects.filter(goodstype_id=goodstype_obj_id)
# 	goods_dic_list = []
# 	for goods_obj in goods_obj_list:
# 		dic = {'name': goods_obj.name, 'price': goods_obj.price, 'img': goods_obj.logo}
# 		goods_dic_list.append(dic)
# 	return JsonResponse(goods_dic_list, safe=False)
# from rest_framework import generics
# from rest_framework import mixins
# class GoodsAjaxView(generics.ListAPIView):
#     serializer_class = GoodsSerializers
#
#     def get_queryset(self):
#         id = self.request.GET.get('goodstype_id')
#         goods_obj_list = models.Goods.objects.filter(goodstype_id=id)
#         return goods_obj_list
#
#     def get_serializer_context(self):
#         return {
#             'view': self
#         }
def goods_detail(request):
	goods_obj_id = request.GET.get('id')
	goods_obj = Goods.objects.get(id=goods_obj_id)
	return render(request, 'buyer/detail.html', locals())

def add_cart(request):
	buyer_obj_id = request.COOKIES.get('buyer_id')
	if buyer_obj_id:
		goods_id = request.GET.get('goods_id')
		number = request.GET.get('number')
		car_obj = Car.objects.filter(goods_id=goods_id, buyer_id=buyer_obj_id).first()

		if car_obj:
			car_obj.goods_num += int(number)
			car_obj.save()
		else:
			goods_obj = Goods.objects.get(id=goods_id)
			car_obj = Car()
			car_obj.goods_id = goods_id
			car_obj.goods_price = goods_obj.price
			car_obj.goods_name = goods_obj.name
			car_obj.goods_num = int(number)
			car_obj.goods_img = goods_obj.logo.name
			car_obj.store_id = goods_obj.store.id
			car_obj.buyer_id = buyer_obj_id
			car_obj.save()
		dic = {'status': '添加购物车成功!'}
	else:
		dic = {'code': 0}
	return JsonResponse(dic)

def my_goodscar(request):
	buyer_id = request.COOKIES.get('buyer_id')
	car_obj_list = Car.objects.filter(buyer_id=buyer_id)
	car_dic_list = []
	for car_obj in car_obj_list:
		dic = {}
		price = car_obj.goods_price
		number = car_obj.goods_num
		xiaoji = price * number
		dic['xiaoji'] = xiaoji
		dic['car_obj'] = car_obj
		car_dic_list.append(dic)


	return render(request, 'buyer/cart.html', locals())

def change_goodscar_num(request):
	car_id = request.GET.get('car_id')
	car_obj = Car.objects.get(id=car_id)
	car_obj.goods_num += 1
	car_obj.save()
	dic = {'status': 'ok'}
	return JsonResponse(dic)

def minus_goodscar_num(request):
	car_id = request.GET.get('car_id')
	car_obj = Car.objects.get(id=car_id)
	car_obj.goods_num -= 1
	car_obj.save()
	dic = {'status': 'ok'}
	return JsonResponse(dic)

def delete_car(request):
	car_id = request.GET.get('id')
	car_obj = Car.objects.get(id=car_id)
	car_obj.delete()
	return redirect('/buyer/my_goodscar/')

import datetime
def place_order(request):
	times = datetime.datetime.now()
	buyer_id = request.COOKIES.get('buyer_id')
	address_obj = BuyerAddress.objects.filter(buyer_id=buyer_id, status=True).first()
	car_id_list = request.POST.getlist('shoppingcarids')
	order = Order()
	order.order_no = times.strftime('%Y%m%d%H%M%S')
	order.order_date = times
	if address_obj:
		order.order_address = address_obj.address + '(' + address_obj.name + ' 收)' + address_obj.phone
	else:
		order.order_address = ''
	order.order_total_num = 0
	order.buyer_id = request.COOKIES.get('buyer_id')
	order.save()
	for car_id in car_id_list:
		car_obj = Car.objects.filter(id=car_id).first()
		order_detail = OrderDetail()
		order_detail.goods_name = car_obj.goods_name
		total = car_obj.goods_num * car_obj.goods_price
		order_detail.goods_total_price = total
		order_detail.goods_num = car_obj.goods_num
		order_detail.goods_price = car_obj.goods_price
		order_detail.goods_img = car_obj.goods_img
		order_detail.order_id = order.id
		order_detail.save()
		order.order_total_num += order_detail.goods_num
		order.order_total_price += order_detail.goods_total_price
		order.save()
		car_obj.delete()
	orders_obj = Order.objects.filter(id=order.id).first()
	return render(request, 'buyer/place_order.html', locals())

def now_buy(request):
	times = datetime.datetime.now()
	buyer_id = request.COOKIES.get('buyer_id')
	address_obj = BuyerAddress.objects.filter(buyer_id=buyer_id, status=True).first()
	if buyer_id:
		order = Order()
		order.order_no = times.strftime('%Y%m%d%H%M%S')
		order.order_date = times
		if address_obj:
			order.order_address = address_obj.address + '(' + address_obj.name + ' 收)' + address_obj.phone
		else:
			order.order_address = ''
		order.order_total_num = 0
		order.buyer_id = request.COOKIES.get('buyer_id')
		order.save()
		address_obj = BuyerAddress.objects.filter(buyer_id=buyer_id, status=True).first()
		goods_id = request.GET.get('goodsid')
		goods_num = request.GET.get('number')
		goods_obj = Goods.objects.get(id=goods_id)
		order_detail_obj = OrderDetail()
		order_detail_obj.goods_name = goods_obj.name
		order_detail_obj.goods_num = goods_num
		order_detail_obj.goods_price = goods_obj.price
		order_detail_obj.goods_total_price = goods_obj.price * int(goods_num)
		order_detail_obj.goods_img = goods_obj.logo
		order_detail_obj.order_id = order.id
		order_detail_obj.save()
		order.order_total_num = goods_num
		order.order_total_price = int(goods_num) * goods_obj.price
		order.save()
		orders_obj = Order.objects.filter(id=order.id).first()
		return render(request, 'buyer/place_order.html', locals())
	else:
		return redirect('/buyer/login/')



def usercenter(request):
	buyer_id = request.COOKIES.get('buyer_id')
	if buyer_id:
		seller_obj = Buyer.objects.get(id=buyer_id)
		address_obj_list = BuyerAddress.objects.filter(buyer_id=buyer_id)
		return render(request, 'buyer/user-center-info.html', locals())
	else:
		return redirect('/buyer/login/')

def add_address(request):
	name = request.POST.get('shoujianren')
	address = request.POST.get('xiangxiaddress')
	email = request.POST.get('youbian')
	phone = request.POST.get('phone')
	buyer_id = request.COOKIES.get('buyer_id')
	address_obj_list = BuyerAddress.objects.filter(buyer_id=buyer_id)
	if address_obj_list:
		address_obj_list.update(status=False)
	buyer_address = BuyerAddress()
	buyer_address.name = name
	buyer_address.address = address
	buyer_address.email = email
	buyer_address.phone = phone
	buyer_address.buyer_id = buyer_id
	buyer_address.status = True
	buyer_address.save()
	return redirect('/buyer/usercenter/')

def change_address_status(request):
	buyer_id = request.COOKIES.get('buyer_id')
	id = request.GET.get('id')
	BuyerAddress.objects.filter(buyer_id=buyer_id).update(status=False)
	address_obj = BuyerAddress.objects.get(id=id)
	address_obj.status = True
	address_obj.save()
	return JsonResponse({'status': 'ok'})

def edit_address(request):
	address_obj_id = request.GET.get('id')
	address_obj = BuyerAddress.objects.get(id=address_obj_id)
	if request.method == 'POST':
		name = request.POST.get('name')
		address = request.POST.get('detail')
		email = request.POST.get('youbian')
		phone = request.POST.get('phone')
		address_obj.name = name
		address_obj.address = address
		address_obj.email = email
		address_obj.phone = phone
		address_obj.save()
		return redirect('/buyer/usercenter/')
	return render(request, 'buyer/edit-address.html', locals())

def delete_address(request):
	id = request.GET.get('id')
	address_obj = BuyerAddress.objects.get(id=id)
	address_obj.delete()
	return redirect('/buyer/usercenter/')

def my_orders(request):
	buyer_id = request.COOKIES.get('buyer_id')
	orders_obj_list = Order.objects.filter(buyer_id=buyer_id)
	for orders_obj in orders_obj_list:
		if orders_obj.order_address == '':
			address_obj = BuyerAddress.objects.filter(status=True, buyer_id=buyer_id).first()
			orders_obj.order_address = address_obj.address + ' (' + address_obj.name + " 收) " + address_obj.phone
			orders_obj.save()
	return render(request, 'buyer/myorders.html', locals())

def yzm():
	return random.randint(1000, 9999)

def register_email_ajax(request):
	dic_msg = {'status': 'success', 'data': ''}
	email_name = request.GET.get('email')
	code = yzm()
	try:
		email = EmailMultiAlternatives(
			subject='验证码',
			body=str(code),
			from_email='ggbool@163.com',
			to=[email_name]
		)
		email.send()
	except:
		dic_msg['data'] = '邮箱不正确'
		dic_msg['status'] = 'error'
	else:
		check_obj = CheckEmail()
		check_obj.email = email_name
		check_obj.code = code
		check_obj.date = datetime.datetime.now()
		check_obj.save()
	finally:
		return JsonResponse(dic_msg)

def register_email(request):
	dic = {'email_name_error': '', 'code_error': '', 'code_time_out': ''}
	if request.method == 'POST':
		email = request.POST.get('emailname')
		code = request.POST.get('code')
		password = request.POST.get('userpass')
		print(email, code, password)
		check_obj = CheckEmail.objects.filter(email=email).first()
		print(check_obj.code)
		if check_obj:
			check_code = check_obj.code
			if code == check_code:
				starttime = check_obj.date
				endtime = datetime.datetime.now()
				print(starttime, endtime)
				zztime = endtime - starttime
				print(zztime.seconds)
				if zztime.seconds < 120:
					buyer_obj = Buyer()
					buyer_obj.name = email
					buyer_obj.password = password
					buyer_obj.email = email
					buyer_obj.phone = 'null'
					buyer_obj.address = 'null'
					buyer_obj.save()
					check_obj.delete()
					return redirect('/buyer/login/')
				else:
					dic['code_time_out'] = '验证码失效!'
					check_obj.delete()
			else:
				dic['code_error'] = '验证码错误'
		else:
			dic['email_name_error'] = '获取验证码邮箱与当前邮箱不一致'
	return render(request, 'buyer/register_email.html', {'dic': dic})

import time
from django.views.decorators.cache import cache_page
@cache_page(10)
def cache_test(request):
	ctime = time.time()
	return render(request, 'buyer/cache_test.html', {'time': ctime})



