from django.contrib import admin
from rsa import sign
from library.models import book,users,available_books,book_transaction,searchitem,Sign,reserve,reserved_book

admin.site.register(book)
admin.site.register(users)
admin.site.register(available_books)
admin.site.register(book_transaction)
admin.site.register(searchitem)
admin.site.register(Sign)
admin.site.register(reserve)
admin.site.register(reserved_book)
# Register your models here.
