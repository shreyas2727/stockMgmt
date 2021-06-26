from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Stock
from .forms import StockForm

import requests
import json



# Create your views here.

# pk_e64399ea88d14b0ba03fba21376a6367 
# pk_e64399ea88d14b0ba03fba21376a6367

def home(request):
    import requests
    import json


    if request.method == "POST":

        ticker = request.POST['ticker'] #comes from search form in base.html
        api_request = requests.get("https://sandbox.iexapis.com/stable/stock/"+ticker+"/quote?token=Tpk_bd77f9d1c76948c0a1f1f25d72928ecc")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error!!!!!"

        context = {
        'api':api
        }
        return render(request,'home.html',context)


    else:

        context = {
            'ticker':"Enter ticker symbol above"
        }
        return render(request,'home.html',context)


def about(request):
    context = {

    }
    return render(request,'about.html',context)


def add_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,"Stock has been added")
            return redirect('add_stock')

    else:
        # show all tickers from db
        ticker = Stock.objects.all()

        # getting the info of added stock into table by connecting to api
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://sandbox.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token=Tpk_bd77f9d1c76948c0a1f1f25d72928ecc")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error!!!!!"

        context = { 
            'ticker':ticker,
            'output':output
        }
        return render(request,'add_stock.html',context)


def delete(request,pk):
    item = Stock.objects.get(id=pk)
    item.delete()
    messages.success(request,'stock has been deleted!!')
    return redirect('delete_stock')


def delete_stock(request):
    ticker = Stock.objects.all()
    context = {
        'ticker':ticker
    }
    return render(request,'delete_stock.html',context)