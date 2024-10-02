from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')  

def post_detail(request, id):
    # Lógica para obtener el post por id y renderizar la plantilla
    pass
