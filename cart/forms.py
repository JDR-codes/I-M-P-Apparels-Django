from django import forms
from . models import CartItems

class AddCartForm(forms.ModelForm):
    class Meta:
        model = CartItems
        fields = ['quantity' , 'size']

    def __init__(self, *args, **kwargs):
        size_choices = kwargs.pop('size_choices')
        super(AddCartForm, self).__init__(*args, **kwargs)
        self.fields['size'].widget = forms.Select(choices=size_choices)

class CouponApplyForm(forms.Form):
    code = forms.CharField(label='Coupon code', max_length=50)