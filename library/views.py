from datetime import date,timedelta
import smtplib
import email,math
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import reserve, reserved_book, users,book_transaction,available_books,book,invoice_history,searchitem,Sign
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
import re
import time
from datetime import datetime, timedelta
from datetime import date

# Create your views here.
def library_home_view(request):
    return render(request,"home/home.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        if len(Sign.objects.filter(username=username))==1:
            user=Sign.objects.filter(username=username).values_list("password").get()[0]
            if user==password:
                return redirect('/home')
            else:
                return render(request,'home/login.html')
        else:
            return render(request,'home/login.html')
    return render(request,'home/login.html')
@ csrf_exempt
def all_books(request):
    books=book.objects.all()
    books={"books":books}
    return render(request,"book/book.html",books)

def add_user(request):
    return render(request,"user/add_user.html")

@ csrf_exempt
def create_user(request):
    
    first_name=request.POST["firstname"]
    last_name=request.POST["lastname"]
    user_name=first_name+" "+last_name
    email=request.POST["email"]
    gender=request.POST["gender"]
    mobile_no=request.POST["mob"]
    category=request.POST["category"]
    user_id=request.POST["user_id"]
    limit=0
    duration=0
    penalty=0
    count=0
    if category=="Under Graduate":
        limit=2
        duration=1
    elif category=="Post Graduate":
        limit=4
        duration=1
    elif category=="Research Scholar":
        limit=6
        duration=3
    elif category=="Faculty Member":
        limit=10
        duration=6

    users.objects.create(user_name=user_name,gender=gender,email=email,mobile=mobile_no,category=category,limit=limit,duration=duration,penalty=penalty,count=count,user_id=user_id)
    return HttpResponseRedirect("/")

def all_user_view(request):
    user=users.objects.all()
    user_dict={"users":user}
    return render(request,"user/all_user.html",user_dict)


@ csrf_exempt
def edit_user(request):
    userid=request.POST["edit_user_detail"]
    name=users.objects.get(pk=userid).user_name.split()
    if(len(name)==1):
        name.append(" ")
    user={"user":users.objects.get(pk=userid),"firstname":name[0],"lastname":name[1]}
    return render(request,"user/edit_user.html",user)

@ csrf_exempt
def update_user(request):
    id=request.POST["id"]
    user=users.objects.get(pk=id)
    user.email=request.POST["email"]
    user.mobile=request.POST["mob"]
    user.save()
    return HttpResponseRedirect("/")


@ csrf_exempt
def profile_view(request):
    id=request.POST["id"]
    name=users.objects.get(pk=id).user_name.split()[0]
    user_id=users.objects.filter(pk=id).values_list("user_id").get()[0]
    books_issued=book_transaction.objects.filter(user_id=user_id)
    reserve_book=reserved_book.objects.filter(user_id=user_id)
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued,"reserve_book":reserve_book}
    return render(request,"user/profile_view.html",user)


@ csrf_exempt
def add_book_to_user(request):
    id=request.POST["id"]
    user_id=users.objects.filter(pk=id).values_list("user_id").get()[0]
    # print(user_id)
    isbn=request.POST["isbn"]
    title=available_books.objects.filter(ISBN=isbn).values_list("title").get()[0]
    cover_url=book.objects.filter(title=title).values_list("cover_url").get()[0]
    issue_date=date.today()
    deadline=issue_date - timedelta(days = 1)
    # deadline=issue_date+relativedelta(months=users.objects.filter(user_id=user_id).values_list("duration").get()[0])
    # print(deadline,title,issue_date)
    count=users.objects.filter(pk=id).values_list("count").get()[0]
    limit=users.objects.filter(pk=id).values_list("limit").get()[0]
    print(count,limit)
    if count<limit:
        book_transaction.objects.create(user_id=users.objects.get(id=id) ,ISBN=isbn,title=title,issue_date=issue_date,deadline=deadline,cover_url=cover_url)
        available_books.objects.filter(ISBN=isbn).delete()
        book_added=book.objects.get(title=title)
        book_added.copies-=1
        book_added.save()
        u=users.objects.get(pk=id)
        u.count+=1
        u.last_activity_date=date.today()

        u.save()
    books_issued=book_transaction.objects.filter(user_id=user_id)
    name=users.objects.get(pk=id).user_name.split()[0]
    reserve_book=reserved_book.objects.filter(user_id=user_id)
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued,"reserve_book":reserve_book}
    # user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued}
    return render(request,"user/profile_view.html",user)

@ csrf_exempt
def reserve_book_to_user(request):
    id=request.POST["id"]
    user_id=users.objects.filter(pk=id).values_list("user_id").get()[0]
    # print(user_id)
    isbn=request.POST["isbn"]
    title=reserved_book.objects.filter(ISBN=isbn).values_list("title").get()[0]
    cover_url=book.objects.filter(title=title).values_list("cover_url").get()[0]
    issue_date=date.today()
    # deadline=issue_date - timedelta(days = 1)
    deadline=issue_date+relativedelta(months=users.objects.filter(user_id=user_id).values_list("duration").get()[0])
    # print(deadline,title,issue_date)
    count=users.objects.filter(pk=id).values_list("count").get()[0]
    limit=users.objects.filter(pk=id).values_list("limit").get()[0]
    print(count,limit)
    if count<limit:
        book_transaction.objects.create(user_id=users.objects.get(id=id) ,ISBN=isbn,title=title,issue_date=issue_date,deadline=deadline,cover_url=cover_url)
        reserved_book.objects.filter(ISBN=isbn).delete()
        book_added=book.objects.get(title=title)
        book_added.copies-=1
        book_added.save()
        u=users.objects.get(pk=id)
        u.count+=1
        u.last_activity_date=date.today()

        u.save()
    books_issued=book_transaction.objects.filter(user_id=user_id)
    name=users.objects.get(pk=id).user_name.split()[0]
    reserve_book=reserved_book.objects.filter(user_id=user_id)
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued,"reserve_book":reserve_book}
    # user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued}
    return render(request,"user/profile_view.html",user)


@ csrf_exempt
def delete_book(request):
    isbn=request.POST["isbn"]
    transaction_user_id=book_transaction.objects.filter(ISBN=isbn).values_list("user_id").get()[0]
    id=users.objects.filter(user_id=transaction_user_id).values_list("id").get()[0]
    title=book_transaction.objects.filter(ISBN=isbn).values_list("title").get()[0]

    return_date=date.today()
    deadline=book_transaction.objects.filter(ISBN=isbn).values_list("deadline").get()[0]
    r=(return_date-deadline).days
    print(isbn)
    u=users.objects.get(pk=id)
    if r>0:
        u.penalty+=r
    u.count-=1
    u.last_activity_date=date.today()
    u.save()

    reserve_book=reserve.objects.filter(title=title).first()
    print("r",reserve_book)
    if reserve_book!=None:
        reserved_book.objects.create(ISBN=isbn,title=title,user_id=reserve_book.user_id,username=reserve_book.username)
        reserve_book.delete()
    else:
        available_books.objects.create(title=title,ISBN=isbn)
        book_added=book.objects.get(title=title)
        book_added.copies+=1
        book_added.save()
    book_transaction.objects.get(ISBN=isbn).delete()
    user_id=users.objects.filter(pk=id).values_list("user_id").get()[0]
    books_issued=book_transaction.objects.filter(user_id=user_id)
    name=users.objects.get(pk=id).user_name.split()[0]
    reserve_book=reserved_book.objects.filter(user_id=user_id)
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued,"reserve_book":reserve_book}
    # user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued}
    return render(request,"user/profile_view.html",user)

from .thread import *
@ csrf_exempt
def send_reminder(request):
    # send_email_to_user.delay()
    send_email_to_user().start()
    # transaction=book_transaction.objects.all()
    # # server = smtplib.SMTP_SSL(smtp_server_domain_name, port, context=ssl_context)
    # # 222222222222222
    # # s = smtplib.SMTP('smtp.gmail.com', 587)
    # # s.starttls()
    # # s.login("website.tester.django@gmail.com", "bikibiki")
    # for t in transaction:
    #     return_date=date.today()
    #     deadline=t.deadline
    #     r=(return_date-deadline).days
    #     # print(return_date,deadline,r,t.ISBN)
    #     if r>0:
    #         message = str(t.title)+" book has been over_due !! try to return it ASAP"+"\n"+"The deadline was: "+str(t.deadline)
    #         # sending the mail
    #         #    email-password-----umhltstpuxcwmjcz
    #         # s.sendmail("website.tester.django@gmail.com", "bikisahoo02@gmail.com", message)
    #         user_id=str(t.user_id)
    #         u=users.objects.filter(user_id=user_id).values_list("email").get()[0]
    #         send_mail("library book overdue", message, "librarytester250@gmail.com", [u], fail_silently=True)
    #         # terminating the session
    return HttpResponseRedirect("/home/")
    # return redirect('/')


@ csrf_exempt
def bill_view(request):
    id=request.POST["id"]
    user=users.objects.get(pk=id)
    invoice=invoice_history.objects.count()
    user={"user":user,"invoice":invoice+1}
    return render(request,"invoice/invoice.html",user)

@csrf_exempt
def bill_paid(request):
    id=request.POST["id"]
    user_id=users.objects.get(pk=id).user_id
    penalty=users.objects.get(pk=id).penalty
    user=users.objects.get(pk=id)
    user.penalty=0
    user.last_activity_date=date.today()
    user.save()
    pay_date=date.today()
    invoice_history.objects.create(user_id=user_id,penalty=penalty,pay_date=pay_date)
    books_issued=book_transaction.objects.filter(user_id=user_id)
    name=users.objects.get(pk=id).user_name.split()[0]
    reserve_book=reserved_book.objects.filter(user_id=user_id)
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued,"reserve_book":reserve_book}
    # user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued}
    return render(request,"user/profile_view.html",user)


@ csrf_exempt
def searching(request):
    print(request.POST["url"])
    searchid=request.POST["search"]
    a=re.compile(f'({searchid})+')
    ebook=users.objects.get_queryset()
    n=users.objects.count()
    i=1
    searchitem.objects.all().delete()
    li1=[]
    for e in ebook:
        li1.append(e.user_id)

    for i in range(n):
        id2=li1[i]
        e=users.objects.get(user_id=id2)
        l=a.findall(str(e.user_id))
        if len(l)!=0:
            user_name=users.objects.get(user_id=e.user_id)
            # id1=title1.id
            email=users.objects.get(user_id=e.user_id).email
            category=users.objects.get(user_id=e.user_id).category
            searchitem.objects.create(user_name=user_name,email=email,category=category,user_id=e.user_id)
    return HttpResponseRedirect('/users/search_item/search_item_view')


def searchview(request):
    li=[]
    for u in searchitem.objects.all():
        li.append(users.objects.get(user_id=u.user_id))
    user_dict={"users":li}
    return render(request,"user/all_user.html",user_dict)

@ csrf_exempt
def book_profile(request):
    id=request.POST["id"]
    books=book.objects.get(pk=id)
    title=books.title
    print(title)
    available_book=available_books.objects.filter(title=title)
    books={"books":books,"available_book":available_book}
    return render(request,"book/book_profile.html",books)

@ csrf_exempt
def send_book(request):
    userid=request.POST["user_id"]
    id1=request.POST["id"]
    # email=users.objects.get(user_id=user_id).email
    # print(id,user_id,email)
    books=book.objects.get(pk=id1)
    # title=books.title
    # send_mail("E-book drive link", "You can download the book "+str(title)+" from the following link "+str(books.ebook_url), "website.tester.django@gmail.com", [email], fail_silently=True)
    # print(title)

    send_reminder11(userid,id1).start()

    available_book=available_books.objects.filter(title=title)
    books={"books":books,"available_book":available_book}
    return render(request,"book/book_profile.html",books)




@ csrf_exempt
def reserve_book(request):
    id=request.POST["id"]
    user_id=users.objects.filter(pk=id).values_list("user_id").get()[0]
    username=users.objects.filter(pk=id).values_list("user_name").get()[0]
    # print(user_id)
    title=request.POST["title"]
    title=title.lower()
    reserve.objects.create(user_id=user_id,username=username,title=title)
    # aaa
    print(title)
    # cover_url=book.objects.filter(title=title).values_list("cover_url").get()[0]
    # issue_date=date.today()
    # # deadline=issue_date - timedelta(days = 1)
    # deadline=issue_date+relativedelta(months=users.objects.filter(user_id=user_id).values_list("duration").get()[0])
    # # print(deadline,title,issue_date)
    # count=users.objects.filter(pk=id).values_list("count").get()[0]
    # limit=users.objects.filter(pk=id).values_list("limit").get()[0]
    # print(count,limit)
    # if count<limit:
    #     book_transaction.objects.create(user_id=users.objects.get(id=id) ,ISBN=isbn,title=title,issue_date=issue_date,deadline=deadline,cover_url=cover_url)
    #     available_books.objects.filter(ISBN=isbn).delete()
    #     book_added=book.objects.get(title=title)
    #     book_added.copies-=1
    #     book_added.save()
    #     u=users.objects.get(pk=id)
    #     u.count+=1
    #     u.save()
    books_issued=book_transaction.objects.filter(user_id=user_id)
    name=users.objects.get(pk=id).user_name.split()[0]
    uu=users.objects.get(pk=id)
    uu.last_activity_date=date.today()
    uu.save()
    reserve_book=reserved_book.objects.filter(user_id=user_id)
    user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued,"reserve_book":reserve_book}
    # user={"user":users.objects.get(pk=id),"name":name,"book_issued":books_issued}
    return render(request,"user/profile_view.html",user)