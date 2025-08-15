from django.shortcuts import render
from logging import exception
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib import messages #import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Buyer, Transaction, Product, TransactionItems

# Create your views here.
def index(request):
	user = request.user
	buyer_profile = Buyer.objects.all()
	transaction_history = Transaction.objects.all()
	context = {
		"user": user,
		"buyers": buyer_profile,
		"transactions": transaction_history
	}
	return render(request, 'index.html', context)

def indexV2(request):
	user = request.user
	context = {
		"user": user
	}

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You are now logged in.")
			return redirect('/indexV2')
		else:
			messages.error(request, "Invalid username or password.")
	else:
		messages.error(request, "Please log in to continue.")

	return render(request, 'indexV2.html', context=context)

def buyerpage(request):
	buyer_fname = request.GET.get('fname')
	buyer_lname = request.GET.get('lname')

	buyer_data = Buyer.objects.get(firstname=buyer_fname, surname=buyer_lname)
	buyer_id = buyer_data.user_id
	transaction_data = Transaction.objects.filter(buyer=buyer_id)

	transactions_total_price = []
	for data in transaction_data:
		for item in data.item_list.all():
			item_price = item.product.price
			item_amount = item.amount
			total_price = item_price * item_amount
			transactions_total_price.append(total_price)

	products = Product.objects.all()

	if request.method == 'POST':
		product_id = request.POST.get('product')
		amount = request.POST.get('amount')

		if product_id:
			print("product ID:", product_id)
			# Step 1: Create transaction with buyer
			transaction = Transaction.objects.create(buyer=buyer_data)
			# Step 2: Assign products using .set()
			transaction.product.add(product_id)
			return redirect(request.META.get('HTTP_REFERER', '/'))

	context = {
		"buyer_data": buyer_data,
		"transaction_data": transaction_data,
		"products": products,
		"all_total_price": transactions_total_price
	}

	return render(request, 'buyerpage.html', context)

def buyerpageV2(request):
	# Buyer Data
	buyer_fname = request.GET.get('fname')
	buyer_lname = request.GET.get('lname')
	buyer_data = Buyer.objects.get(firstname=buyer_fname, surname=buyer_lname)
	buyer_id = buyer_data.user_id

	# Product Data
	products = Product.objects.all()

	# Transaction Data
	transaction_data = Transaction.objects.filter(buyer=buyer_id)

	# Grand Total
	grandtotal = 0
	for t_data in transaction_data:
		subtotal = t_data.subtotal
		grandtotal += subtotal

	if request.method == 'POST':
		product_ids = request.POST.getlist('product_ids')

		subtotal = 0
		total_transaction_item = []
		for product_id in product_ids:
			quantity = int(request.POST.get(f"quantity_{product_id}"))
			product_obj = products.get(product_id=product_id)
			if quantity > 0:
				transaction_item = TransactionItems.objects.create(product=product_obj, 
																   amount=quantity, 
																   total_price=product_obj.price*quantity)
				total_transaction_item.append(transaction_item)
				subtotal += product_obj.price*quantity
		
		transaction = Transaction.objects.create(buyer=buyer_data)
		transaction.item_list.set(total_transaction_item)
		transaction.subtotal = subtotal
		transaction.save()
		return redirect(request.META.get('HTTP_REFERER', '/'))


	context = {
		"buyer_data": buyer_data,
		"products": products,
		"transaction_data": transaction_data,
		"grandtotal": grandtotal
	}

	return render(request, 'buyerpageV2.html', context)

def login_new(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/indexV2")
