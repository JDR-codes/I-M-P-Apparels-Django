from django.shortcuts import redirect, render
from . forms import UserProfileForm, UserAddressForm
from django.contrib.auth import get_user_model
from . models import UserProfile, SavedAddress
from django.contrib.auth.decorators import login_required
from cart.models import Coupon, UserCoupon
User = get_user_model()
# Create your views here.
def create_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print('hii')
            profile = form.save(commit=False)  
            profile.user = request.user        
            profile.save()                     
            return redirect('user-profile') 
        else:
            print(form.errors)

    
    form = UserProfileForm()
    return render(request,'create_profile.html',{'form' : form})

def edit_profile_view(request):
    profile = UserProfile.objects.get(user = request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
        
    form = UserProfileForm(instance=profile)
    return render(request,'edit_profile.html',{'form':form})

@login_required(login_url='login')
def user_profile_view(request):
    msg = None
    user_profile = None
    user = User.objects.get(username = request.user)
    try:
        user_profile = UserProfile.objects.get(user = user)
    except:
        msg = "Profile hasn't created yet"
    return render (request,'user_profile.html',{'user_profile' : user_profile, 'msg' : msg})

def add_address_view(request):
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            form.save()
            return redirect('saved-address')
    
    form = UserAddressForm()
    return render(request,'add_address.html',{'form' : form})


def saved_address_view(request):
    return render(request,'saved_address.html',{'addresses' : SavedAddress.objects.filter(user = request.user)})

def delete_address_view(request,id):
    address = SavedAddress.objects.get(id = id)
    address.delete()
    return redirect('saved-address')

def coupon_list_view(request):
    return render(request, 'coupons.html',{'coupons' : Coupon.objects.all()})