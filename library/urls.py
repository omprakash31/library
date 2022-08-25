from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view ),
    path('home/',views.library_home_view ),
    path('add_user/',views.add_user ),
    path('add_user/create_user/',views.create_user ),
    path('users/',views.all_user_view),
    path('books/',views.all_books),
    path('users/edit_user/',views.edit_user),
    path('users/edit_user/update_user/',views.update_user),
    path('users/profile_view/',views.profile_view),
    path('users/profile_view/add_book/',views.add_book_to_user),
    path('users/profile_view/delete_book/',views.delete_book),
    path('users/profile_view/reserve_book/',views.reserve_book),
    path('users/profile_view/reserve_book_to_user/',views.reserve_book_to_user),
    path('users/send_reminder/',views.send_reminder),
    path('users/profile_view/bill/',views.bill_view),
    path('users/profile_view/bill/bill_paid/',views.bill_paid),
    path('users/search_item/',views.searching),
    path('users/search_item/search_item_view/',views.searchview),
    path('books/book_profile/',views.book_profile),
    path('books/book_profile/send_book',views.send_book),
]