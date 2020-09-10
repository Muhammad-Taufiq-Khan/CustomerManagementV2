from django.shortcuts import render, redirect
from django.http import HttpResponse

#from django.contrib import messages
# Create your views here.
from .models import *
from .forms import OrderForm,CustomerForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users,admin_only

#for automate authentication, login,logout
from django.contrib.auth import authenticate, login, logout

#for flash message
from django.contrib import messages

#to restrict Unauthenticated login
from django.contrib.auth.decorators import login_required

#for setting group
from django.contrib.auth.models import Group

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method=='POST':
		form= CreateUserForm(request.POST)
		if form.is_valid():
			user=form.save()
			#getting user name:
			username= form.cleaned_data.get('username')
			#setting user's instant group name:
			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#after registration rederect to login page
			return redirect ('login')
			
	context={'form':form}
	return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
	if request.method =='POST':
		username= request.POST.get('username')
		password= request.POST.get('password')
		user= authenticate(request,password=password,username=username)

		if user is not None:
			login(request,user)
			return redirect ('home')
		else:
			messages.info(request,"Username Or Password don't match")
	context={}
	return render(request,'accounts/login.html',context)

def logoutPage(request):
	logout(request)
	return redirect ('login')


@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	out_for_delivery=orders.filter(status='Out for delivery').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending,'out_for_delivery':out_for_delivery }

	return render(request, 'accounts/dashboard.html', context)


def userPage(request):
	context={}
	return render (request, 'accounts/user.html', context)

	 

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@admin_only

def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter=OrderFilter (request.GET,queryset=orders)
	orders=myFilter.qs

	context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@admin_only

def createOrder(request):
	form=OrderForm()
	if request.method=="POST":
		form= OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
@admin_only

def createCustomer(request):
	f=CustomerForm()
	if request.method == "POST":
		f=CustomerForm(request.POST)
		if f.is_valid():
			f.save()
			return redirect('/')
	context={'form':f}
	return render(request, 'accounts/create_customer.html',context)

@login_required(login_url='login')
def updateOrder(request, pk):
	order=Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method =="POST":
		form=OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context={'form':form}
	return render (request, 'accounts/order_form.html',context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order=Order.objects.get(id= pk)
	if request.method=="POST":
		order.delete()
		return redirect('/')

	context={'item':order}
	return render (request, 'accounts/delete.html',context)