from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Vote, Comment
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from django.core.exceptions import PermissionDenied
import json
from collections import defaultdict
from products.serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import permissions
import simplejson
import mimetypes
import functools
from rest_framework.views import APIView

def ajax_login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return JsonResponse('Unauthorized', status=401, safe=False)
    return wrapper


def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products':products})

@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.image = request.FILES['image']
            product.icon = request.FILES['icon']
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else: 
            return render(request, 'products/create.html', {'error' : 'Please fill all the fields before submitting.'})

    else:
        return render(request, 'products/create.html')


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})


@csrf_exempt
@ajax_login_required
def upvote(request, product_id):
    if request.method == 'POST':
        try:
            vote = Vote.objects.get(productId=product_id,userId=request.user)
        except Vote.DoesNotExist:
            vote = None
        if vote is None:
            product = get_object_or_404(Product, pk=product_id)
            vote = Vote(productId=product, userId=request.user)
            vote.save()
            product.votes_total = int(request.POST['click_count'])
            product.save()
            return redirect('/products/' + str(product.id))
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=product_id)
        data = {
            'vote': product.votes_total
        }
        print(data)
        return JsonResponse(data)


@login_required
def downvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total -= 1
        product.save()
        return redirect('/products/' + str(product.id))


@csrf_exempt
@ajax_login_required
def comments(request, product_id):
    if request.method == 'POST':
        comment = Comment()
        comment.productId = get_object_or_404(Product, pk=product_id)
        comment.userId = request.user
        comment.username = request.user
        comment.comment = request.POST['comment']
        print(comment.comment)
        comment.save()
        return redirect('/products/' + str(comment.productId))
        
    if request.method == 'GET':
        comments = Comment.objects.filter(userId=request.user, productId=product_id).values()
        latest_comment = comments.last()
        
        data = {
            'latest':latest_comment,
            'user':str(request.user), 
        }
        return JsonResponse(data)

def commentall(request, product_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(productId=product_id)
        serializer_class = CommentSerializer(comments, many=True)
        return JsonResponse(serializer_class.data, safe=False)
