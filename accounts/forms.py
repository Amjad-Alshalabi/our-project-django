from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date

YEARS= [x for x in range(1940,2021)]

class SignUpForm(UserCreationForm):
    # birth_date = forms.DateField(
    #     widget=forms.SelectDateWidget(years=YEARS) ,  
    #     initial=date.today , 
    #     required=True)
    class Meta:
        model = User
        fields = (
        'username' , 
        'first_name' , 
        'last_name' ,
        # 'birth_date' , 
        'email', 
        'password1' , 
        'password2' , )
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # this for make this fields require from user #
        # username , password1 and password2 is required by default
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        # this to set placeholder , it's just HTML5 :) 
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-Password'

    # setup unique email and tell user if it duplicate !!
    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            msg = 'This email address already exists.'
            self.add_error('email',msg)