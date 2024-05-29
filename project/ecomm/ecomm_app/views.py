from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product, Cart,Order
from django.db.models import Q
import random

# Create your views here.

def about(request):
    return HttpResponse("This is About page")

def edit(request,rid):   # edit/3   ===>rid=3
    print("Id to be edited is:",rid)
    return HttpResponse("Id to be edited is "+ rid)

def delete(request,x1,x2):  #x1='10', x2='20'
    t=int(x1)+int(x2)   #t=10+20 =>30
    print(t)   #int
    return HttpResponse("Addition of xa and x2 is: "+ str(t))
    #print("Id to be deleted:",rid)
    #return HttpResponse("Id to be deleted is "+ rid)

class SimpleView(View):
    def get(self,request):
        return HttpResponse("Hello from view class")

def hello(request):
    context={}
    context['greet']='good evening, we are learning DTL'
    context['x']=100
    context['y']=20
    context['l']=[10,20,30,40,50,'eclass']
    context['products']=[
        {'id':1,'name':'samsung','cat':'mobile','price':2000}, #i
        {'id':2,'name':'jeans','cat':'clothes','price':700},
        {'id':3,'name':'vivo','cat':'mobile','price':15000},
        {'id':4,'name':'adidas','cat':'shoes','price':3500},
        ]
    return render(request,'hello.html',context)

#---------------- estore project-----------

def home(request):
    #userid=request.user.id   #4
    #print(userid)
    #print("Result is:",request.user.is_authenticated)
    context={}
    p=Product.objects.filter(is_active=True)
    #print(p)
    context['products']=p    # 6 products- objects
    return render(request,'index.html',context)

def product_details(request,pid):  #pid=4
    p=Product.objects.filter(id=pid)
    #print(p)
    context={}
    context['products']=p
    return render(request,'product_details.html',context)

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":# F or F or F=>F
            context['errmsg']="Fields cannot be Empty"
        elif upass != ucpass:
            context['errmsg']="Password & confirm password didn't match"
        else:
          try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User Created Successfully, Please Login"
          except Exception:
                context['errmsg']="User with same username already exists!!!!"
        #return HttpResponse("User created successfully!!")
        return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print(uname,'-',upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields cannot be Empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/')
            else:
                context['errmsg']="Invalid username and password"
                return render(request,'login.html',context)
            #return HttpResponse("Data is fetched")  
    else:
        return render(request,'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/')

def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1&q2)
    print(p)     # 2 objects
    context={}
    context['products']=p    #2 objects
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        #ascending
        col='price'
    else:
        #descending order
        col='-price'
    p=Product.objects.order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    # print(min)
    # print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)   #4th object
        p=Product.objects.filter(id=pid)   #1st object
        #check product exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        print(c)  # queryset[<object 3>] 
        n=len(c)   # 1
        context={}
        if n == 1: 
            context['msg']="Product Already Exist in cart!!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product Added Successfully to Cart!!"
        context['products']=p
        return render(request,'product_details.html',context)
        # return HttpResponse("product added in cart")
    else:
        return redirect('/login')
    
def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)  #uid=2
    # print(c)  # queryset[<object1>, <object2>]
    np=len(c)    #2
    s=0
    for x in c:
         s=s + x.pid.price * x.qty
    print(s)
    context={}
    context['data']=c
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)


def remove(request,cid):   #cid=10
    c=Cart.objects.filter(id=cid)   #id=10
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    print(c)
    print(c[0])
    print(c[0].qty)
    if qv=='1':
        t=c[0].qty + 1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty - 1
            c.update(qty=t)
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id #second=>3
    c=Cart.objects.filter(uid=userid) #uid=3
    #print(c)
    oid=random.randrange(1000,9999)
    #print(oid)
    for x in c:
        #print(x)
        #print(x.pid,"=",x.uid,"-",x.qty)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    context={}
    Orders=Order.objects.filter(uid=request.user.id)
    np=len(Orders) #2
    context['data']=Orders
    context['n']=np
    s=0
    for x in Orders:
        s= s + x.pid.price * x.qty
    context['total']=s
    #return HttpResponse("order placed successfully")
    return render(request,'placeorder.html',context)

def makepayment(request):
    return HttpResponse("In makepayment funtion")


    







