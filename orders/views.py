import razorpay
from django.shortcuts import redirect, render
from cart.models import CartItems, Cart
from . models import *
from products.models import Size
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from user_profile.models import SavedAddress

# Create your views here.

def checkout_view(request):
    if request.method == 'POST':
        final_price = int(float(request.POST.get('final_price')))
    user = Cart.objects.get(user = request.user)
    cart_items = CartItems.objects.filter(cart = user)
    addresses = SavedAddress.objects.filter(user = request.user)

    order = Order.objects.create(
        user = request.user,
        total_price = final_price
    )

    for item in cart_items:
        OrderItem.objects.create(
            order = order,
            product = item.product,
            quantity = item.quantity,
            size = item.size
        )

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

    razorpay_order = client.order.create({
        'amount' : int(final_price * 100),
        'currency' : 'INR',
    })
    order.razorpay_id = razorpay_order['id']
    order.save()
    print(razorpay_order)

    context = {
        'cart_items': cart_items,
        'saved_addresses' : addresses,
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': final_price,
        'currency': 'INR',
        'callback_url': '/paymenthandler/'
    }

    return render(request, 'checkout.html', context)

@csrf_exempt
def payment_handler_view(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            params_dict = {
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }

            result = client.utility.verify_payment_signature(params_dict)
            if result is None:
                # Mark order as paid
                order = Order.objects.get(razorpay_id=order_id)
                order.is_paid = True
                order.save()
                
                for item in order.orderitem_set.all():
                    size = Size.objects.get(pcode = item.product, size = item.size)
                    size.stock -= item.quantity
                    size.save()

                CartItems.objects.filter(cart = order.user).delete()
                return render(request, 'payment_status.html', {'status': 'success'})
            else:
                return render(request, 'payment_status.html', {'status': 'failed'})
        except Exception as e:
            print(str(e))
            return render(request, 'payment_status.html', {'status': 'failed'})
