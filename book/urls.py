from django.urls import path
from . import views

urlpatterns=[
    path('home/',views.home_page,name='home_page'),
    path('book/',views.book_list,name='book_list'),
    path('book/<int:book_id>/',views.book_detail,name='book_detail'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('view_cart',views.cart,name='view_cart'),
    path('increment/',views.increment_cart,name='increment_cart'),
    path('delete/', views.delete_from_cart, name='delete_from_cart'),
    path('decrement/',views.decrement_cart,name='decrement_cart'),
    path('logout/', views.logout_page, name='logout_page'),
]