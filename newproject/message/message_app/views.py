from django.shortcuts import render,HttpResponse,redirect
#from message_app.models import Msg
from .models import Msg

# Create your views here.
def testing(request):
    return HttpResponse("Hello linked successfully")

def create(request):
    if request.method=='POST':   #get==post
        #print("method is:",request.method)
        n=request.POST['uname']
        mail=request.POST['uemail']
        mob=request.POST['mobile']
        msg=request.POST['msg']
        m=Msg.objects.create(name=n,email=mail,mobile=mob,msg=msg)
        m.save()
        #print("Data is:",n)
        #return HttpResponse("Insert data into database table")
        return redirect('/')
    else:
        #print("method is:",request.method)
        return render(request,'create.html')
    
def dashboard(request):
    m=Msg.objects.all()
    #print(m)
    context={}
    context['data']=m
    return render(request,'dashboard.html',context)
    #return HttpResponse("Data Fetched from database")

def delete(request,rid):
    #print("Id to deleted:",rid)
    m=Msg.objects.filter(id=rid)  #id=3
    #print(m)    #<QuerySet [<Msg: Msg object (3)>]>
    m.delete()    
    return redirect('/')
    #return HttpResponse("Id to be deleted:"+ rid)

def edit(request,rid):
    if request.method=='POST':
        #fetch new values and update record
        un=request.POST['uname']     
        umail=request.POST['uemail']  
        umob=request.POST['mobile'] 
        umsg=request.POST['msg']    
        m=Msg.objects.filter(id=rid) #1st record
        m.update(name=un,email=umail,mobile=umob,msg=umsg)
        return redirect('/')
    else:
        #display form with old values
        m=Msg.objects.get(id=rid)  #6th
        print(m)     #Msg: Msg object (6)
        context={}
        context['data']=m
        return render(request,'edit.html',context)

