from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Vote
from django.views.decorators.csrf import csrf_exempt
def home(request):
    products = Product.objects
    return render(request, 'products/home.html')

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
@login_required
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