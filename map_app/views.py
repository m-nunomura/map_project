from django.shortcuts import render,redirect
from .models import AddressList,QuakeList,QuakeDetail,CityList,StoreList
from django.db.models import Q
from . import consts
import requests
import urllib
from .forms import AddressForm, StoreForm
import re
import urllib.request
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

#--------------------------------------------------------------------------
#トップ画面-----------------------------------------------------------------
@login_required
def index(request):
    addresslist = AddressList.objects.all()
    quakelist = QuakeList.objects.all()
    quakedetaillist = QuakeDetail.objects.all()
    storelist = StoreList.objects.all()
    address_query = request.GET.get("input_address")
    level_query = request.GET.get('input_level')

    if request.method == 'POST':

        #Create処理（物件）
        if "create_address" in request.POST:
            name = request.POST["name"]
            address = request.POST["address"]
            category = request.POST["category"]
            year = request.POST["year"]
            level = request.POST["level"]
            coordinates = get_coordinates(address)
            latitude = coordinates[1]
            longitude = coordinates[0]
            address = AddressList(name=name,
                            address=address,
                            category=StoreList.objects.get(id=category),
                            year=year,
                            level=level,
                            latitude=latitude,
                            longitude=longitude)
            address.save()
        
        #Create処理（加盟店）
        elif "create_store" in request.POST:
            name = request.POST["name"]
            address = request.POST["address"]
            coordinates = get_coordinates(address)
            latitude = coordinates[1]
            longitude = coordinates[0]
            store = StoreList(name=name,
                            address=address,
                            latitude = latitude,
                            longitude=longitude)
            store.save() 

    addressform = AddressForm()
    storeform = StoreForm()
            
    #物件名でサーチ
    if address_query:
        addresslist = addresslist.filter(name__icontains=address_query)

    #レベルでサーチ
    if level_query:
        addresslist = addresslist.filter(level = level_query)

    return render(request, "map_app/index.html", {"addresslist":addresslist,
                                                  "quakelist":quakelist,
                                                  "quakedetaillist":quakedetaillist,
                                                  "storelist":storelist,
                                                  "addressform":addressform,
                                                  "storeform":storeform})





#--------------------------------------------------------------------------
#Update処理（address：物件、store：加盟店）----------------------------------
@login_required
def address_update(request, pk):
    address = AddressList.objects.get(id=pk)
    form = AddressForm(instance=address)
    if request.method == "POST":        
        address = AddressList.objects.get(id=pk)
        address.name = request.POST.get("name")
        address.address = request.POST.get("address")
        address.category = StoreList.objects.get(id=request.POST.get("category"))
        address.year = request.POST.get("year")
        coordinates = get_coordinates(address.address)
        address.latitude = coordinates[1]
        address.longitude = coordinates[0]
        address.save()
        return redirect("/map")
    return render(request, "map_app/update.html",{"form":form})



@login_required
def store_update(request, pk):
    store = StoreList.objects.get(id=pk)
    form = StoreForm(instance=store)
    if request.method == "POST":
        store = StoreList.objects.get(id=pk)
        store.name = request.POST.get("name")
        store.address = request.POST.get("address")
        coordinates = get_coordinates(store.address)
        store.latitude = coordinates[1]
        store.longitude = coordinates[0]
        store.save()
        return redirect("/map")
    return render(request, "map_app/update.html",{"form":form})


@login_required
def address_delete(request, pk):
    address = AddressList.objects.get(id=pk)
    form = AddressForm(instance=address)
    if request.POST:
        address.delete()
        return redirect("/map")
    return render(request, "map_app/delete.html")


@login_required
def store_delete(request, pk):
    address = StoreList.objects.get(id=pk)
    if request.POST:
        address.delete()
        return redirect("/map")
    return render(request, "map_app/delete.html")





#--------------------------------------------------------------------------
#地震情報の登録-------------------------------------------------------------
@login_required
def create_quake(request):
    quakeDetails = []
    if request.method == "POST":
        #対象URLにリクエストを送る
        input_url = request.POST["xml_url"]
        res = urllib.request.urlopen(input_url).read()
        soup = BeautifulSoup(res)

        #地震に関する情報のみを抽出
        search = re.compile(".*VXSE.*")

        for vxse in soup.find_all(text=search):
            #対象URLにリクエストを送る
            res = urllib.request.urlopen(vxse).read()
            soup = BeautifulSoup(res)

            #イベントIDを取得
            event_id = soup.find("eventid").text
            
            #モデルに同じイベントIDがあればスキップする
            if QuakeList.objects.filter(event_id = event_id).exists():
                continue
            else:
                for content in soup.find_all("body"):
                    earthquake = content.find("earthquake")

                    #earthquakeの情報がない地震情報は対象外
                    if earthquake is not None:

                        #地震の各種情報を取得
                        name = earthquake.find("name").text                     #地震発生場所
                        origintime = earthquake.find("origintime").text         #地震発生時刻
                        origintime = origintime.replace("T"," ")
                        origintime = origintime.replace("+09:00","")
                        coordinate = earthquake.find("jmx_eb:coordinate").text  #地震発生座標
                        lat = coordinate[1:coordinate[1:].find("+") + 1]
                        lon = coordinate[coordinate[1:].find("+") + 2:coordinate[1:].find("+") + 7]
                        lat = int(lat[0:2])+(int(lat[3:])/60)+(0/3600)
                        lon = int(lon[0:3])+(int(lon[4:])/60)+(0/3600)
                        magnitude = earthquake.find("jmx_eb:magnitude").text    #マグニチュード

                        quakelist = QuakeList(event_id = event_id,
                                            name = name,
                                            magnitude = magnitude,
                                            date = origintime,
                                            latitude = lat,
                                            longitude = lon)
                        #quakelists.append(quakelist)
                        quakelist.save()

                    intensity = content.find("intensity")

                    #intensityの情報がない地震情報は対象外
                    if intensity is not None: 
                        for pref in intensity.find_all("pref"):

                            #地震対象都道府県から対象の市町村を取得
                            for city in pref.find_all("city"):
                                code = city("code")[0].text  
                                code = code[0:len(code)-2]
                                list = CityList.objects.get(city_code = code)
                                prefectuer = list.prefecture_name
                                city_name = list.city_name
                                intensity = city("maxint")[0].text         #対象市町村の最大震度
                                address = prefectuer+city_name
                                coordinates = get_coordinates(address)
                                latitude = coordinates[1]
                                longitude = coordinates[0]

                                quakedetail = QuakeDetail(event_id = QuakeList.objects.get(event_id=event_id),
                                                        prefecture = prefectuer,
                                                        city = city_name,
                                                        intensity = intensity,
                                                        latitude = latitude,
                                                        longitude = longitude)
                                quakeDetails.append(quakedetail)
                                
        #QuakeList.objects.bulk_create(quakelists)
        QuakeDetail.objects.bulk_create(quakeDetails)
    return render(request,"map_app/create_quake.html")


#-------------------------------------------
#住所→座標
def get_coordinates(address):
    makeUrl = consts.makeUrl
    s_quote = urllib.parse.quote(address)
    response = requests.get(makeUrl + s_quote)
    coordinated = response.json()[0]["geometry"]["coordinates"]
    return coordinated


def delete_address(request,num):
    address = AddressList.objects.get(id = num)
    if request.method == "POST":
        address.delete()
        return redirect("/map")
    params = {
        "title":"delete",
        "id":num,
        "address":address,
    }


