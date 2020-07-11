from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .forms import SignUpForm
from .tokens import account_activation_token
from project.settings import EMAIL_HOST_USER


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        # return redirect('home')  ## here where user have to go after confirm amjad!! 
    else:
        return render(request, 'registration/activation_invalid.html')

def signup(request):
    # profile = models.Profile.objects.get(user_id = 1)
    # print(profile.user)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() # load the profile instance created by the signal
            # user.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('registration/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user)
            })
            send_mail(subject, message, EMAIL_HOST_USER, [user.email], fail_silently = False)
            user = authenticate(username=username, password=password)
            login(request, user)
            # return redirect(reverse('activation_sent_view')) redirect to home
            
            
    else:
        form = SignUpForm()
    return render(request, 'registration/signup1.html', {'form': form})