from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import QrCode
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from django.conf import settings
from qrcode import *
import time
from qr_code.qrcode.utils import QRCodeOptions
import qrcode
def home(request):
    return render(request, 'users/home.html')
def qr_gen(request):
    if request.method == 'POST':
        data = request.POST['data']
        img = qrcode.make(data)
        img_name = 'qr' + str(time.time()) + '.png'
        img.save(settings.MEDIA_ROOT + '/' + img_name)
        return render(request, 'users/index.html', {'img_name': img_name})
    return render(request, 'users/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            adhaar = form.cleaned_data.get('adhaar_no')
            pan = form.cleaned_data.get('pan_no')
            address = form.cleaned_data.get('last_name')
            firstname = form.cleaned_data.get('first_name')
            full ="Name" + "\n" + str(firstname) + "\n"+ "Address" + "\n" + str(address) + "\n"+ "Adhar number" + "\n" + str(adhaar) + "\n" +"Pan number" + "\n" + str(pan)
            img = qrcode.make(full)
            img_name = 'qr' + str(time.time()) + '.png'
            img.save(settings.MEDIA_ROOT + '/' + img_name) 
            messages.success(request, f'Account created for {username} {adhaar}')
            return render(request, 'users/index.html', {'img_name': img_name})
            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    # def form_valid(self, form):
    #     remember_me = form.cleaned_data.get('remember_me')

    #     if not remember_me:
    #         # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
    #         self.request.session.set_expiry(0)

    #         # Set session as modified to force data updates/cookie to be saved.
    #         self.request.session.modified = True

    #     # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
    #     return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

def banklogin(request):
    if request.method == 'POST1':
        print("hii")
    return render(request, 'users/profile.html')