from django.urls import path
from . import views

urlpatterns = [
   path('api/posts/', views.api_posts, name='api_posts'),
   path('api/posts/<int:id>/', views.api_post_detail, name='api_post_detail'),
   path('api/js', views.api_json, name='json_api'),
   path('', views.publicaciones, name='publicaciones'),
   path('crear/', views.crear_post, name='crear_post'),
]

