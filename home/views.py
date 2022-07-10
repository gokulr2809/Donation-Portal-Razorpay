from http import client
from tabnanny import check
from unicodedata import name
from django.shortcuts import render
import razorpay
from razorpay.client import Client
from .models import donate
from django.views.decorators.csrf import csrf_exempt
from razorpay.utility import *

def home(request):
    if request.method == "POST":
      name = request.POST.get("name")
      amount = int(request.POST.get("amount"))*100
      client = Client(auth=("your public key", "your private key")) 
      payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture': '1'})
      actual = int(request.POST.get("amount"))
      don = donate(name = name,amount = amount,payment_id = payment['id']) 
      don.save()
      return render(request,"process.html",{'payment':payment,'actual': actual})
    return render(request,"index.html")
@csrf_exempt
def sucess(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        data = {}
        for key,values in a.items():
            if key == "razorpay_order_id":
                order_id = values
                data['razorpay_order_id'] = values
            elif key == "razorpay_payment_id":
                data['razorpay_payment_id'] = values
            elif key == "razorpay_signature":
                data['razorpay_signature'] = values

        user = donate.objects.filter(payment_id = order_id)
        client = razorpay.Client(auth=("your public key", " your private key")) 
        check = client.utility.verify_payment_signature(data)
        if not check:
            return render(request,'fail.html')
        user.status = True
        user.save()
    return render(request,"sucess.html",{'id':order_id})
