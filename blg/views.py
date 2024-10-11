from django.http import HttpResponse
from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth import login as lg , logout , authenticate
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserProfileForm , AuthorProfileForm , PostForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Comment, Author


# Create your views here.

def index(request):
    recent_posts = Post.objects.filter(published=True).order_by('-created_at')[:6]
    
    if request.user.is_authenticated:
        messages.info(request, f"¡Bienvenido, {request.user.username}!")
    
    print(recent_posts)  # Verifica si hay posts capturados
    return render(request, 'index.html', {'recent_posts': recent_posts})


def post_detail(request, id):
    # Lógica para obtener el post por id y renderizar la plantilla
    pass


def login(request):
    # Verificar si la solicitud es de tipo POST (cuando el usuario envía el formulario)
    if request.method == 'POST':
        # Crea una instancia del formulario de autenticación con los datos del POST
        form = AuthenticationForm(request, data=request.POST)
        
        # Validar si el formulario es correcto (credenciales válidas)
        if form.is_valid():
            # Obtener los datos de usuario del formulario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password') 
            
            # Autenticar el usuario con el método 
            user = authenticate(request, username=username, password=password)
            
            # Si el usuario es autenticado correctamente
            if user is not None:
                # Inicia sesión con el método login
                lg(request, user)
                # Redirige al usuario a la página de inicio 
                return redirect('index')
            else:
                # Si no se encuentra al usuario, agrega un mensaje de error
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            # Si el formulario no es válido, agrega un mensaje de error
            messages.error(request, 'Datos inválidos.')
    
    # Si la solicitud es GET (el usuario simplemente visita la página), muestra el formulario
    else:
        form = AuthenticationForm()

    # Renderiza la página de login con el formulario
    return render(request, 'user/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        # Capturar los campos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        bio = request.POST.get('bio')  

        # Verificación si el nombre de usuario o email ya existen
        if User.objects.filter(username=username).exists():
            messages.error(request, f'{username} ya existe en nuestra base de datos')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, f'{email} ya existe en nuestra base de datos')
            return redirect('register')

        # Crear el usuario
        usuario = User.objects.create_user(username=username, email=email, password=password)

        # Crear el perfil de autor asociado, con la biografía
        Author.objects.create(user=usuario, bio=bio)

        messages.success(request, 'Usuario creado correctamente')
        
        # Redirigir al usuario a la página de inicio de sesión
        return redirect('login')  

    return render(request, 'user/register.html', {})


def profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        author_form = AuthorProfileForm(request.POST, instance=request.user.author)

        if user_form.is_valid() and author_form.is_valid():
            user_form.save()
            author_form.save()
            return redirect('index')  # Redirige después de guardar

    else:
        user_form = UserProfileForm(instance=request.user)
        author_form = AuthorProfileForm(instance=request.user.author)

    return render(request, 'user/profile.html', {
        'user_form': user_form,
        'author_form': author_form,
    })




def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # Obtener el objeto Author correspondiente al usuario actual
            author = get_object_or_404(Author, user=request.user)
            post.author = author  # Asignar la instancia de Author
            post.save()
            return redirect('index')  # Redirigir a la página principal después de crear el post
    else:
        form = PostForm()
    
    return render(request, 'user/create_post.html', {'form': form})



class PostDetailView(DetailView):
    model = Post
    template_name = 'user/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(approved=True)
        return context

    def post(self, request, *args, **kwargs):
        # Verifica si el usuario está autenticado antes de procesar el comentario
        if not request.user.is_authenticated:
            return redirect('login')  # Redirige al inicio de sesión si no está autenticado
        
        post = self.get_object()
        content = request.POST.get('content')
        author = Author.objects.get(user=request.user)
        Comment.objects.create(post=post, author=author, content=content)
        return redirect(self.request.path)




def cerrar(request):
    if request.user.is_authenticated:
        # mensaje de despedida
        messages.info(request, f"¡Hasta luego, {request.user.username}! Has cerrado sesión.")
        logout(request)  # Cierra la sesión del usuario
    return redirect('index')  # Redirige al usuario a la página de inicio