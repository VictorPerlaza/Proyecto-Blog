# Importaciones necesarias
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect  # Para manejar vistas y redirecciones
from django.contrib.auth import login as lg, logout, authenticate  # Funciones de autenticación
from django.contrib import messages  # Para mostrar mensajes de feedback al usuario
from django.contrib.auth.models import User  # Modelo de usuario predeterminado de Django
from django.contrib.auth.decorators import login_required  # Decorador para proteger vistas
from django.views.generic import DetailView  # Vista basada en clase para detalles
from django.contrib.auth.forms import AuthenticationForm  # Formulario de autenticación de Django
from .forms import UserProfileForm, AuthorProfileForm, PostForm  # Formularios personalizados
from .models import Post, Comment, Author, Notification, Reaction  # Modelos utilizados
from django.core.paginator import Paginator # Paginación 
import pytz  # Biblioteca para manejar zonas horarias


def index(request):
    posts = Post.objects.filter(published=True).order_by('published')[:6]  # Filtra solo los posts publicados y toma los 6 más recientes
    if request.user.is_authenticated:
        # Si el usuario está autenticado, muestra un mensaje de bienvenida y cuenta notificaciones no leídas
        messages.info(request, f"¡Bienvenido, {request.user.username}!")
        unread_notifications_count = request.user.notifications.filter(is_read=False).count()
        # Pasar el conteo de notificaciones no leídas si es necesario
        return render(request, 'index.html', {'recent_posts': posts, 'unread_notifications_count': unread_notifications_count})
    
    return render(request, 'index.html', {'recent_posts': posts})  # Renderiza la plantilla con los posts


# Vista para iniciar sesión
def login(request):
    if request.method == 'POST':
        # Si es una solicitud POST, intenta autenticar al usuario con los datos proporcionados
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                lg(request, user)  # Inicia sesión
                return redirect('index')  # Redirige a la página principal
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Datos inválidos.')
    else:
        # Si es GET, muestra el formulario vacío
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

# Vista para registrar un nuevo usuario
def register(request):
    if request.method == 'POST':  # Si se envió el formulario
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        bio = request.POST.get('bio', '')  # Biografía opcional
        avatar = request.FILES.get('avatar')  # Avatar opcional
        # Verifica si el nombre de usuario o correo ya existen
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ya hay una cuenta registrada con este email.')
            return redirect('register')
        # Crea el usuario y el autor asociado
        user = User.objects.create_user(username=username, email=email, password=password)
        Author.objects.create(user=user, bio=bio, avatar=avatar)
        messages.success(request, 'Tu cuenta ha sido creada exitosamente.')
        return redirect('login')  # Redirige a la página de inicio de sesión
    return render(request, 'user/register.html')  # Muestra el formulario

# Vista protegida para editar el perfil del usuario
@login_required
def profile(request):
    user_form = UserProfileForm(instance=request.user)  # Formulario para el modelo User
    author_form = AuthorProfileForm(instance=request.user.author)  # Formulario para el modelo Author
    if request.method == 'POST':
        # Si se envió el formulario, valida y guarda los datos
        user_form = UserProfileForm(request.POST, instance=request.user)
        author_form = AuthorProfileForm(request.POST, request.FILES, instance=request.user.author)
        current_password = request.POST.get('current_password')  # Contraseña actual
        new_password = request.POST.get('new_password')  # Nueva contraseña
        confirm_password = request.POST.get('confirm_password')  # Confirmación
        if user_form.is_valid() and author_form.is_valid():
            if current_password and request.user.check_password(current_password):
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()  # Guarda los cambios
                else:
                    messages.error(request, "Las nuevas contraseñas no coinciden.")
                    return render(request, 'user/profile.html', {'user_form': user_form, 'author_form': author_form})
            user_form.save()
            author_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('profile')  # Redirige al perfil
    return render(request, 'user/profile.html', {'user_form': user_form, 'author_form': author_form})

# Vista para mostrar detalles del perfil de otro usuario

def profile_detail_users(request, user_id):
    # Si el user_id coincide con el usuario autenticado, redirige al perfil del usuario autenticado
    if user_id == request.user.id:
        profile_user = request.user.author  # Accede al perfil del usuario autenticado (su autor)
    else:
        # Si el user_id no coincide, busca al autor por ID
        profile_user = get_object_or_404(Author, user__id=user_id)  # Obtiene el autor relacionado con el user_id

    posts = profile_user.post_set.all()  # Obtiene los posts del autor

    return render(request, 'user/profile_detail.html', {
        'profile_user': profile_user,  # Usuario cuyo perfil se está viendo
        'posts': posts,
        'user': request.user  # Usuario autenticado
    })

# Vista protegida para crear un post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Formulario para crear un post
        if form.is_valid():
            post = form.save(commit=False)
            author = get_object_or_404(Author, user=request.user)  # Obtiene el autor asociado al usuario
            post.author = author
            post.save()
            form.save_m2m()  # Guarda relaciones ManyToMany
            return redirect('index')  # Redirige a la página principal
    else:
        form = PostForm()  # Muestra el formulario vacío
    return render(request, 'user/create_post.html', {'form': form})

# Clase para mostrar los detalles de un post
class PostDetailView(DetailView):
    model = Post
    template_name = 'user/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        # Agrega los comentarios aprobados al contexto
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(approved=True)
        return context

    def post(self, request, *args, **kwargs):
        # Permite agregar comentarios a un post
        if not request.user.is_authenticated:
            return redirect('login')  # Si no está autenticado, redirige al inicio de sesión
        post = self.get_object()  # Obtiene el post actual
        content = request.POST.get('content')  # Contenido del comentario
        author = Author.objects.get(user=request.user)  # Autor del comentario
        Comment.objects.create(post=post, author=author, content=content)
        return redirect(self.request.path)  # Recarga la página

# Otras funciones están estructuradas de manera similar
# Se explican en detalle sus respectivas responsabilidades

def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        author = request.user.author
        content = request.POST.get('content')
        
        # Crear el comentario
        comment = Comment.objects.create(post=post, author=author, content=content)
        
        # Crear una notificación para el autor de la publicación
        Notification.objects.create(
            user=post.author.user,
            message=f"{request.user.username} comentó en tu publicación '{post.title}'"
        )
        
        return redirect('post_detail', post_id=post.id)


def search(request):
    query = request.GET.get('q', '')  # Obtiene la consulta de la barra de búsqueda
    posts = Post.objects.filter(title__icontains=query) if query else None
    users = User.objects.filter(username__icontains=query) if query else None

    context = {
        'query': query,
        'posts': posts,
        'users': users
    }
    return render(request, 'user/buscar.html', context)

@login_required
def react_to_post(request, post_id, reaction_type):
    post = get_object_or_404(Post, id=post_id)
    
    # Verifica si el usuario ya ha reaccionado al post
    existing_reaction = Reaction.objects.filter(post=post, user=request.user).first()
    
    if existing_reaction:
        # Si ya reaccionó, actualiza el tipo de reacción
        existing_reaction.reaction_type = reaction_type
        existing_reaction.save()
    else:
        # Si no ha reaccionado, crea una nueva reacción
        Reaction.objects.create(post=post, user=request.user, reaction_type=reaction_type)
    
    return redirect('post_detail', pk=post.id)

@login_required
def notifications(request):
    notifications = request.user.notifications.filter(is_read=False)
    return render(request, 'user/notificaciones.html', {'notifications': notifications})

def exp_posts(request):
    posts = Post.objects.all().order_by('published')  # Ordena por fecha (más reciente primero)
    paginator = Paginator(posts, 9)  # Muestra 9 publicaciones por página

    page_number = request.GET.get('page')  # Obtén el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtén la página actual

    return render(request, 'user/ex-post.html', {'page_obj': page_obj})

def cerrar(request):
    if request.user.is_authenticated:
        # mensaje de despedida
        messages.info(request, f"¡Hasta luego, {request.user.username}! Has cerrado sesión.")
        logout(request)  # Cierra la sesión del usuario
    return redirect('index')  # Redirige al usuario a la página de inicio