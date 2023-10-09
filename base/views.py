from django.shortcuts import render, redirect
from django.conf import settings
import aiohttp
from requests import Session
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor
from zeep.client import Client
from zeep.transports import Transport
import random
from cryptography.fernet import Fernet
from asgiref.sync import sync_to_async
# Create your views here.

def home(request):
    return render(request, 'home.html')

def createsupplier(request):
    me = "etwryreerueuu"
    key = settings.ENC_KEY
    print("key", key)
    encpass = Fernet(key).encrypt(me.encode())
    
    if request.method == "POST":
        
        myAction = request.POST.get("myAction")
        name = request.POST.get("name")
        contactname = request.POST.get("contactname")
        email = request.POST.get("email")
        contactemail = request.POST.get("contactemail")
        countryregioncode = request.POST.get("countryregioncode")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("cpassword")
        phone = request.POST.get("phone")
        postalcode = request.POST.get("postalcode")
        postaladdress = request.POST.get("postaladdress")
        city = request.POST.get("city")
        token = random.randint(10000, 99999)
        if password == confirmpassword:
            key = settings.ENC_KEY
            print(key)
            encpass = Fernet(key).encrypt(password.encode())
            print(encpass)
            session = Session()
            session.auth = HTTPBasicAuth(settings.REQUEST_UID, settings.REQUEST_PWD)
            with ThreadPoolExecutor() as ex:
                client = Client(settings.BASE_URL, transport = Transport(session=session))
                response = ex.submit(
                    client.service["FnProspectiveSupplierSignup"],
                    "",
                    name, 
                    email, 
                    countryregioncode, 
                    postaladdress, 
                    postalcode, 
                    city, 
                    contactname, 
                    phone, 
                    contactemail, 
                    encpass,
                    token,
                    myAction
                ).result()
                print(response)

    return render(request, "createsupplier.html")

async def loginsupplier(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        async with aiohttp.ClientSession() as session:
            async with session.get(settings.O_DATA + f"?$filter=Email%20eq%20%27{email}%27", auth = aiohttp.BasicAuth(settings.REQUEST_UID, settings.REQUEST_PWD)) as response:
                result = await response.json()
                print(result["value"])
                if result["value"][0]["Email"] == email:
                    key = settings.ENC_KEY
                    dencpass = Fernet(key).decrypt(result["value"][0]["SerialID"]).decode()
                    if dencpass == password:
                        await sync_to_async(request.session.__setitem__)("email", result["value"][0]["Email"])
                        await sync_to_async(request.session.__setitem__)("No", result["value"][0]["No"])
                        print("correct password")
                        return redirect("supplierdetails")
                    else:
                        print("wrong password")
    return render(request, "loginsupplier.html")

async def supplierdetails(request):
    ctx = []
    try:
        email = await sync_to_async(request.session.__getitem__)("email")
        No = await sync_to_async(request.session.__getitem__)("No")
        print(email, No)
        async with aiohttp.ClientSession() as session:
            async with session.get(settings.O_DATA + f"?$filter=No%20eq%20%27{str(No)}%27", auth = aiohttp.BasicAuth(settings.REQUEST_UID, settings.REQUEST_PWD)) as response:
                result = await response.json()
                ctx = result["value"][0]
                print(settings.O_DATA + f"?$filter=No%20eq%20%27{str(No)}%27")
    except:
        return redirect("login")
    return render(request, 'supplierdetails.html', {"ctx" : ctx})