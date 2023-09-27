from django.shortcuts import render
from django.http import HttpResponse
from.models import *
from datetime import datetime
from django.db import connection


# Create your views here.
def index(request):
    data=category.objects.all().order_by('id')[0:6]
    sliderdata=slider.objects.all().order_by('id')[0:3]
    pdata=myproduct.objects.all().order_by('id')[0:6]
    opdata=myproduct.objects.filter(total_discount__gte=30)

    md={"cdata":data,"sdata":sliderdata,"pdata":pdata,"opdata":opdata}
    return render(request,"user/index.html",md)
    
    #print(data)
def about(request):
    return render(request,template_name="user/aboutus.html")
def contact(request):
    if request.method=="POST":
       a1=request.POST.get('name')
       a2=request.POST.get('email')
       a3=request.POST.get('mobile')
       a4=request.POST.get('message')
       #print(a1,a2,a3,a4)
       #x=contactus(Name=a1,Email=a2,Mobile=a3,Message=a4).save()
       # print(x)
       contactus(Name=a1,Email=a2,Mobile=a3,Message=a4).save()
       return HttpResponse("<script>alert('Thank you Your Data have saved Successfully');location.href='/user/contact'</script>")
    return render(request,template_name="user/contactus.html")
def signup(request):
    if request.method=='POST':
        name=request.POST.get('name')
        mobile=request.POST.get('mobile')
        email=request.POST.get('email')
        passwd=request.POST.get('passwd')
        address=request.POST.get('address')
        pic=request.FILES['fu']
        x=register.objects.all().filter(email=email).count()
        if x==1:
            return HttpResponse("<script>alert('You are already register');location.href='/user/signup'</script>")
        else:
            register(name=name,mobile=mobile,email=email,passwd=passwd,address=address,profile=pic).save()
            return HttpResponse("<script>alert('You are register succsessful');location.href='/user/signup'</script>")

    return render(request,template_name="user/signup.html")


def signin(request):
    if request.method=="POST":
        email=request.POST.get('email')
        passwd=request.POST.get('passwd')
        x=register.objects.filter(email=email,passwd=passwd).count()
        if x==1:
            x=register.objects.filter(email=email,passwd=passwd)
            request.session['user']=email
            request.session['userpic']=str(x[0].profile)
            request.session['username']=str(x[0].name)
            user=request.session.get('user')
            cartitems=cart.objects.filter(userid=user).count()
            request.session['cartitems']=cartitems

            return HttpResponse("<script>('login seccessful..');location.href='/user/signin'</script>")
        else:
            return HttpResponse("<script>('your username or password is incorrect');location.href='/user/signin'</script>")
    return render(request,template_name="user/signin.html")

def signout(request):
    if request.session.get('user'):
        del request.session['user']
        del request.session['userpic']
        return HttpResponse("<script>('Signout seccessful..');location.href='/user/index'</script>")
    return render(request,template_name='user/signout.html')    
            
def product(request):
    subcatid=request.GET.get('sid')
    print(subcatid)
    sdata=subcategory.objects.all().order_by('id')
    if subcatid is not None:
        pdata=myproduct.objects.all().filter(subcategory_name=subcatid)
    else:
        pdata=myproduct.objects.all().order_by('id')
    md={"subcat":sdata,"pdata":pdata}
    return render(request,"user/product.html",md)

def myprofile(request):
    user=request.session.get('user')
    rdata=""
    if request.method=='POST':
        name=request.POST.get('name')
        mobile=request.POST.get('mobile')
        passwd=request.POST.get('passwd')
        address=request.POST.get('address')
        pic=request.FILES['fu']
        register(name=name,email=user,mobile=mobile,passwd=passwd,address=address,profile=pic).save()
        return HttpResponse("<script>('Your Profile is updated seccessful..');location.href='/user/myprofile/'</script>")
        
    if user:
        rdata=register.objects.filter(email=user)
    md={"rdata":rdata}
    return render(request,'user/myprofile.html',md)


def privacy(request):
    return render(request,template_name="user/privacy.html")

def mycart(request):
    user=request.session.get('user')
    if user:
        qt=int(request.GET.get('qt'))#5
        pname=request.GET.get('pname')
        pw=request.GET.get('pw')
        ppic=request.GET.get('ppic')
        price=int(request.GET.get('price'))#50
        total_price=qt*price
        if qt>0:
        #print(qt,pname,ppic,pw,price,total_price)
            cart(userid=user,product_name=pname,quantity=qt,price=price,total_price=total_price,product_picture=ppic,pw=pw,added_date=datetime.now().date()).save()
            cartitems=cart.objects.filter(userid=user).count()
            request.session['cartitems']=cartitems
            return HttpResponse("<script>alert('Your item is added in cart..');location.href='/user/product/'</script>")
        else:
            return HttpResponse("<script>alert('Please increase your card item');location.href='/user/product/'</script>")
            
    return render(request,template_name="user/mycart.html")


def cartitems(request):
    user=request.session.get('user')
    cid=request.GET.get('cid')
    cartdata="";
    if user:
        cartdata=cart.objects.filter(userid=user)
        if cid is not None:
            cart.objects.filter(id=cid).delete()
            cartitems=cart.objects.filter(userid=user).count()
            request.session['cartitems']=cartitems
            return HttpResponse("<script>alert('Your cart item is removed successfully..');location.href='/user/cartitems/'</script>")

    md={"cartdata":cartdata}    
    return render(request,"user/cartitems.html",md)

def morder(request):
    msg=request.GET.get('msg')
    user=request.session.get('user')
    if msg is not None:
        cursor=connection.cursor()
        cursor.execute("insert into user_myorders (product_name,quantity,price,total_price,product_picture,pw,userid,status,order_date) select product_name,quantity,price,total_price,product_picture,pw,'"+str(user)+"','Pending','"+str(datetime.now().date())+"' from user_cart where userid='"+str(user)+"'")
        cart.objects.filter(userid=user).delete()
        cartitems=cart.objects.filter(userid=user).count()
        request.session['cartitems']=cartitems
        return HttpResponse("<script>alert('Your order has placed successfully..');location.href='/user/cartitems/'</script>")

    return render(request,template_name="user/order.html")

def indexcart(request):
    user=request.session.get('user')
    if user:
        qt=int(request.GET.get('qt'))#5
        pname=request.GET.get('pname')
        pw=request.GET.get('pw')
        ppic=request.GET.get('ppic')
        if qt>0:
            price=int(request.GET.get('price'))#50
            total_price=qt*price
            cart(userid=user,product_name=pname,quantity=qt,price=price,total_price=total_price,product_picture=ppic,pw=pw,added_date=datetime.now().date()).save()
            cartitems=cart.objects.filter(userid=user).count()
            request.session['cartitems']=cartitems
            return HttpResponse("<script>alert('Your item is added in cart..');location.href='/user/index/'</script>")
        else:
            return HttpResponse("<script>alert('Please increase your card item');location.href='/user/index/'</script>")
            

    return render(request,template_name="user/index.html")

def orderlist(request):
    oid=request.GET.get('oid')
    user=request.session.get('user')
    pdata=myorders.objects.filter(userid=user,status="Pending")
    adata=myorders.objects.filter(userid=user,status="Accepted")
    ddata=myorders.objects.filter(userid=user,status="Delivered")
    if oid is not None:
        myorders.objects.filter(id=oid)
        return HttpResponse("<script>alert('Your order has been cancel');location.href='/user/orderlist/'</script>")

    mydict={"pdata":pdata,"adata":adata,"ddata":ddata}
    return render(request,"user/orderlist.html",mydict)


def mprofile(request):
    return render(request,template_name='mprofile.html')







