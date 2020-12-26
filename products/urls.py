from django.urls import path, include
from .import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('create', views.create, name='create'), 
    path('<int:product_id>', views.detail, name='detail'), 
    path('<int:product_id>/upvote/', views.upvote, name='upvote'),
    path('<int:product_id>/downvote/', views.downvote, name='downvote'), 
    path('<int:product_id>/comment/', views.comments, name='comment'),
    path('<int:product_id>/comments/', views.commentall, name='comments'),
]
