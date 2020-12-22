from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product

def home(request):
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
            return redirect('home')
        else: 
            return render(request, 'products/create.html', {'error' : 'Please fill all the fields before submitting.'})

    else:
        return render(request, 'products/create.html')





