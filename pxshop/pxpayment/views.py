from django.shortcuts import render
from logging import exception
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib import messages #import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Buyer, Transaction, Product

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
	return redirect("/")
