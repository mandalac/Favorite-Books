from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')


def register(request):
    errors = User.objects.registrationValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashpw)
        messages.info(request, 'The account is created, plese LogIn')
        return redirect('/')

def login (request):
    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, 'Invalid email adress')
        return redirect('/')
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, 'Invalid password')
        return redirect('/')
    else:
        request.session['user_firstName'] = user.first_name
        request.session['user_id'] = user.id
        return redirect('/books')
    return redirect('/')

def logout(request):
    del request.session['user_firstName']
    del request.session['user_id']
    return redirect('/')
    

def books(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Please Log In')
        return redirect('/')
    else:
        context = {
            'all_books' : Book.objects.all(),
            'favorite_user_book' : User.objects.get(id = request.session['user_id'])
        }
        return render(request, 'books.html', context)   

def create_book(request):
    errors = Book.objects.bookValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/books')
    else:
        Book.objects.create(title=request.POST['title'], description=request.POST['description'], uploader = User.objects.get(id = request.session['user_id']) )
        messages.success(request, 'Book is added')
    return redirect('/books')
 
def add_to_favorites(request, book_id):
    User.objects.get(id = request.session['user_id']).favorites.add(Book.objects.get(id=book_id))
    return redirect('/books')

def view_edit_page(request, book_id):
    context = {
        'book' : Book.objects.get(id = book_id),
        'user' : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'edit.html', context)

def update_book(request, book_id):
    errors = Book.objects.bookValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect(f'/books/edit/{book_id}')
    else:
        book = Book.objects.get(id = book_id)
        book.title = request.POST['title']
        book.description = request.POST['description']
        book.save()
        return redirect('/books')

def delete(request, book_id):
    Book.objects.get(id=book_id).delete()
    return redirect('/books')

def view_page(request, book_id):
    context = {
        'book' : Book.objects.get(id = book_id),
        'user' : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'view_book.html', context)

def unFavorite(request, book_id):
    User.objects.get(id = request.session['user_id']).favorites.remove(Book.objects.get(id = book_id))
    return redirect(f'/books/view/{book_id}')