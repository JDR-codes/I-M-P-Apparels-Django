from django.shortcuts import render
from products.models import Products,Size,Categories, AccessoriesCat
# Create your views here.
def homepage_view(request):
    context = {
        'trending' : Products.objects.filter(trending = True),
        'category' : Categories.objects.all(),
        'new' : Products.objects.filter(new = True)
    }
    return render(request,'home.html',context)

def categories_view(request):
    return render(request,'category.html',{'category' : Categories.objects.all()})

def acc_categories_view(request):
    return render(request,'acc_category.html',{'category' : AccessoriesCat.objects.all()})

def contact_us_view(request):
    return render(request,'contactus.html')

def about_us_view(request):
    return render(request,'aboutus.html')