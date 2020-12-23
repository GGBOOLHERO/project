from django.shortcuts import render, HttpResponse, render_to_response, redirect
from seller.models import *
from seller.form import SellerForm
import os

# Create your views here.
def checklogin(func):
	def inner(request):
		seller_name = request.COOKIES.get('seller_name')
		if seller_name:
			return func(request)
		else:
			return redirect('/seller/login/')

	return inner

def login(request):
	msg = ''
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		seller_obj = Seller.objects.filter(username=username, password=password).first()
		if seller_obj:
			response = redirect('/seller/index/')
			response.set_cookie('seller_name', seller_obj.username)
			response.set_cookie('seller_id', seller_obj.id)
			response.set_cookie('seller_headimg', seller_obj.head_img.name)
			return response
		else:
			msg = '账号或密码错误!'
	return render(request, 'seller/login.html', {'msg': msg})

def logout(request):
	response = redirect('/seller/login/')
	response.delete_cookie('seller_name')
	response.delete_cookie('seller_id')
	response.delete_cookie('seller_headimg')
	return response

def register(request):
	sellerform = SellerForm(request.POST, request.FILES)
	if sellerform.is_valid():
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		address = request.POST.get('address')
		gender = request.POST.get('gender')
		img = request.FILES.get('headimg')
		seller = Seller()
		seller.username = username
		seller.password = password
		seller.email = email
		seller.phone = phone
		seller.address = address
		seller.gender = gender
		seller.head_img = img
		seller.save()
		return redirect('/seller/login/')
	return render(request, 'seller/register.html', {'sellerform': sellerform})

@checklogin
def index(request):
	return render(request, 'seller/index.html')

def store(request):
	if request.method == 'POST':
		store_id = request.POST.get('id')
		if store_id:
			name = request.POST.get('shopname')
			address = request.POST.get('shopaddress')
			desc = request.POST.get('shopdesc')
			logo = request.FILES.get('shopimg')
			store_obj = Store.objects.get(id=store_id)
			if logo:
				path = 'static/' + store_obj.logo.name
				try:
					os.remove(path)
				except:
					pass
				store_obj.logo = logo
			store_obj.name = name
			store_obj.address = address
			store_obj.desc = desc
			store_obj.save()
			return redirect('/seller/index/')
		else:
			name = request.POST.get('shopname')
			address = request.POST.get('shopaddress')
			desc = request.POST.get('shopdesc')
			logo = request.FILES.get('shopimg')
			store_obj = Store()
			store_obj.name = name
			store_obj.address = address
			store_obj.desc = desc
			seller_id = request.COOKIES.get('seller_id')
			seller_obj = Seller.objects.get(id=seller_id)
			store_obj.seller = seller_obj
			store_obj.save()
			return redirect('/seller/index/')
	else:
		seller_id = request.COOKIES.get('seller_id')
		seller_obj = Seller.objects.get(id=seller_id)
		try:
			store_obj = seller_obj.store
		except:
			pass
	return render(request, 'seller/store.html', locals())

def goodstype_list(request):
	seller_id = request.COOKIES.get('seller_id')
	seller_obj = Seller.objects.get(id=seller_id)
	goodstype_obj_list = Goods_Type.objects.filter(seller_id=seller_obj.id)
	return render(request, 'seller/goods_type_list.html', locals())

def add_goodstype(request):
	if request.method == "POST":
		seller_id = request.COOKIES.get('seller_id')
		seller_obj = Seller.objects.get(id=seller_id)
		name = request.POST.get('goodstype_name')
		logo = request.FILES.get('goodstype_img')
		goods_type_obj = Goods_Type()
		goods_type_obj.name = name
		goods_type_obj.logo = logo
		goods_type_obj.seller = seller_obj
		goods_type_obj.save()
		return redirect('/seller/goodstype_list/')

def edit_goodstype(request):
	id = request.POST.get('id')
	goodstype_obj = Goods_Type.objects.get(id=id)
	if request.method == 'POST':
		name = request.POST.get('goodstypename')
		logo = request.FILES.get('goodstypeimg')
		goodstype_obj.name = name
		if logo:
			path = 'static/' + goodstype_obj.logo.name
			goodstype_obj.logo = logo
			os.remove(path)
		goodstype_obj.save()
		return redirect('/seller/goodstype_list/')
	return render(request, 'seller/edit_goodstype.html', locals())

def delete_goodstype(request):
	id = request.GET.get('id')
	goodstype_obj = Goods_Type.objects.get(id=id)
	path = 'static/' + goodstype_obj.logo.name
	os.remove(path)
	goodstype_obj.delete()
	return redirect('/seller/goodstype_list/')

def goods_list(request):
	seller_id = request.COOKIES.get('seller_id')
	store_obj = Store.objects.filter(seller_id=seller_id).first()
	goods_obj_list = Goods.objects.filter(store_id=store_obj.id)
	return render(request, 'seller/goods_list.html', locals())

def add_goods(request):
	goodstype_obj_list = Goods_Type.objects.all()
	if request.method == 'POST':
		name = request.POST.get('name')
		price = request.POST.get('price')
		bzq = request.POST.get('bzq')
		scrq = request.POST.get('productdate')
		desc = request.POST.get('desc')
		img = request.FILES.get('goodsimg')
		goodstype_id = request.POST.get('goodstype_id')
		goodstype_obj = Goods_Type.objects.get(id=goodstype_id)
		seller_id = request.COOKIES.get('seller_id')
		store_obj = Store.objects.filter(seller_id=seller_id).first()
		goods_obj = Goods()
		goods_obj.name = name
		goods_obj.price = price
		goods_obj.product_dt = scrq
		goods_obj.shelf_life = bzq
		goods_obj.desc = desc
		goods_obj.logo = img
		goods_obj.goodstype = goodstype_obj
		goods_obj.store = store_obj
		goods_obj.save()
		return redirect('/seller/goods_list/')
	return  render(request, 'seller/add_goods.html', locals())
