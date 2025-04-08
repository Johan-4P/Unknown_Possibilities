from django.shortcuts import render

# Create your views here.

def product(request):
    """ A view to return the products page """
    return render(request, 'product.html')