# views.py
from django.shortcuts import render,redirect,get_object_or_404
from .models import Author, Book,Cart
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home_page(request):
    books = Book.objects.all()[:8]
    authors=Author.objects.all()[:5]
    return render(request, 'home_page.html', {'books': books, 'authors': authors})

def book_list(request):
    books = Book.objects.all()

    if request.GET.get('action') == 'search_title':
        title_search = request.GET.get('title_search', '')
        books = books.filter(title__icontains=title_search)
    else:
        sort_by = request.GET.get('sort_by')

        if sort_by == 'atoz':
            books = books.order_by('title')
        elif sort_by == 'ztoa':
            books = books.order_by('-title')
        elif sort_by == 'pricelow':
            books = books.order_by('price')
        elif sort_by == 'pricehigh':
            books = books.order_by('-price')

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                books = books.filter(price__range=(min_price, max_price))
            except ValueError:
                pass  

        min_pages = request.GET.get('min_pages')
        max_pages = request.GET.get('max_pages')
        if min_pages and max_pages:
            try:
                min_pages = int(min_pages)
                max_pages = int(max_pages)
                books = books.filter(pages__range=(min_pages, max_pages))
            except ValueError:
                pass

        rating = request.GET.getlist('rating')
        if rating:
            books = books.filter(avg_rating__in=rating)

        publisher = request.GET.get('publisher')
        if publisher:
            books = books.filter(publisher__icontains=publisher)

        author_name = request.GET.get('author', '')
        books = books.filter(author__name__icontains=author_name)

        genre = request.GET.get('genre')
        if genre:
            books = books.filter(genre=genre)

        language = request.GET.getlist('language')
        if language:
            books = books.filter(language__in=language)

    return render(request, 'book_list.html', {'books': books})


def book_detail(request,book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user, quantity__gt=0)
    total_items = sum(item.quantity for item in cart)
    total_cost = sum(item.book.price * item.quantity for item in cart)
    context = {
        'cart': cart,
        'total_items': total_items,
        'total_cost': total_cost,
    }
    return render(request, 'view_cart.html', context)

def decrement_cart(request):
    if request.method == 'POST':
        cart_book_id = request.POST.get('book_id')
        cart_book = get_object_or_404(Cart, id=cart_book_id, user=request.user)

        quantity = int(request.POST.get('book_quantity_requested',0))
        quantity -= 1
        quantity = max(quantity, 0)
        if quantity==0:
            delete_cart_item(cart_book)
        cart_book.quantity = quantity
        cart_book.save()

    return redirect('view_cart')

def delete_from_cart(request):
    if request.method=='POST':
        cart_book_id=request.POST.get('book_id')
        book=get_object_or_404(Cart,id=cart_book_id,user=request.user)
        delete_cart_item(book)
    return redirect('view_cart')

def increment_cart(request):
    if request.method=='POST':
        cart_book_id=request.POST.get('book_id')
        cart_book = get_object_or_404(Cart, id=cart_book_id, user=request.user)
        quantity = int(request.POST.get('book_quantity_requested',0))
        quantity+=1
        if quantity==10:
            print('max reached')
        cart_book.quantity=quantity
        cart_book.save()
    return redirect('view_cart')

def delete_cart_item(book):
    if book:
        book.delete()

@login_required
def add_to_cart(request):
    books = Book.objects.all()

    if request.method == 'POST':
        book_id_to_add = request.POST.get('add_to_cart')
        if book_id_to_add:
            book_to_add = get_object_or_404(Book, id=book_id_to_add)
            cart, created = Cart.objects.get_or_create(book=book_to_add, user=request.user)
            if not created:
                cart.quantity += 1
                cart.save()
            else:
                cart.save()
            print(cart.quantity,cart.book,cart.user)
            return redirect('home_page')

    return render(request, 'home_page.html', {'books': books})
            
def logout_page(request):
    logout(request)
    referring_url = request.session.get('referring_url', 'home_page')
    request.session.pop('referring_url', None)
    return redirect(referring_url)