from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login as lg
from django.contrib.auth import authenticate
from django.shortcuts import redirect 
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'index.html')  

def post_detail(request, id):
    # Lógica para obtener el post por id y renderizar la plantilla
    pass


def register(request):
   if request.method == 'POST':
    username = request.POST.get('nombre')
    email = request.POST.get('correo')
    password = request.POST.get('contra')

    if User.objects.filter(username=username).exists():
        messages.error(request, f'{username} ya existe en nuestra database')
        return redirect('register')
       
    if User.objects.filter(email=email).exists():
        messages.error(request, f'{email} ya existe en nuestra database')
        return redirect('register')

    usuario = User.objects.create_user(username, email, password)

    if usuario :
       lg(request,usuario)
       messages.success(request, f'Bienvenido {username}')
       return redirect('juegos')

   return render(request, 'user/register.html', {})