from django.shortcuts import render
from logging import exception
from unicodedata import category
from django.shortcuts import render, redirect
from django.contrib import messages #import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Buyer, Transaction

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

	context = {
		"buyer_data": buyer_data,
		"transaction_data": transaction_data
	}

	return render(request, 'buyerpage.html', context)
