import threading
from .models import book_transaction,users,book
from django.conf import settings
from django.core.mail import send_mail
from datetime import date

class send_email_to_user(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print("started")
        print("email")
        transaction=book_transaction.objects.all()
        for t in transaction:
            return_date=date.today()
            deadline=t.deadline
            r=(return_date-deadline).days
            # print(return_date,deadline,r,t.ISBN)
            if r>0:
                message = str(t.title)+" book has been over_due !! try to return it ASAP"+"\n"+"The deadline was: "+str(t.deadline)
                # sending the mail
                #    email-password-----umhltstpuxcwmjcz
                # s.sendmail("website.tester.django@gmail.com", "bikisahoo02@gmail.com", message)
                user_id=str(t.user_id)
                u=users.objects.filter(user_id=user_id).values_list("email").get()[0]
                send_mail("library book overdue", message, "librarytester250@gmail.com", [u], fail_silently=True)



class send_reminder11(threading.Thread):
    def __init__(self,userid,id):
        self.userid=userid
        self.id=id
        threading.Thread.__init__(self)
    def run(self):
        print("started")
        email=users.objects.get(user_id=self.userid).email
        print(id,email)
        books=book.objects.get(pk=self.id)
        title=books.title
        send_mail("E-book drive link", "You can download the book "+str(title)+" from the following link "+str(books.ebook_url), "librarytester250@gmail.com", [email], fail_silently=True)
        print(title)