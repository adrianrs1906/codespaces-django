from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Post, Comment
from django.shortcuts import get_object_or_404

CARS = [
    {
        "id": 1,
        "name": "Ferrari F8 Spider",
        "price": 340000,
        "description": "Convertible de alto rendimiento con lujo italiano y tecnología de pista.",
        "image": "blog/ferrari-f8.jpg",
    },
    {
        "id": 2,
        "name": "Lamborghini Aventador",
        "price": 420000,
        "description": "Superdeportivo V12 con diseño atrevido y una experiencia de conducción única.",
        "image": "blog/lamborghini-aventador.jpg",
    },
    {
        "id": 3,
        "name": "Bentley Continental GT",
        "price": 265000,
        "description": "Gran turismo de lujo con interiores artesanales y confort insuperable.",
        "image": "blog/bentley-continental.jpg",
    },
]


def publicaciones(request):
    selected_id = request.GET.get("car_id")
    months = request.GET.get("months", "60")
    selected_car = None
    monthly_payment = None

    try:
        months = int(months)
    except (ValueError, TypeError):
        months = 60

    if selected_id:
        selected_car = next((car for car in CARS if str(car["id"]) == str(selected_id)), None)
        if selected_car:
            monthly_payment = round(selected_car["price"] / months, 2)

    # Manejar comentarios
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if name and message:
            Comment.objects.create(name=name, email=email, message=message)
            return redirect("publicaciones")

    comments = Comment.objects.all().order_by('-created_at')

    return render(request, 'blog/publicaciones.html', {
        'cars': CARS,
        'selected_car': selected_car,
        'monthly_payment': monthly_payment,
        'months': months,
        'comments': comments,
    })

def crear_post(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        contenido = request.POST.get("contenido", "")

        if not titulo:
            return render(request, "blog/crear.html", {
                "error": "El título no puede estar vacío"
            })

        Post.objects.create(
            titulo=titulo,
            contenido=contenido
        )
        return redirect("publicaciones")

    return render(request, 'blog/crear.html')

def api_posts(request):
    posts = Post.objects.all().values('id', 'titulo', 'contenido', 'fecha', 'autor')
    return JsonResponse(list(posts), safe=False)

def api_post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    data = {
        'id': post.id,
        'titulo': post.titulo,
        'contenido': post.contenido,
        'fecha': post.fecha,
        'autor': post.autor,
    }
    return JsonResponse(data)

def api_json(request):
    return render(request, 'blog/api.html')