from random import randint
from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from AccountApp.models import User, OTP
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from AccountApp.forms import RegisterForm, OTPVerifyForm, LoginForm, ResetForm


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'AccountApp/register and login.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['user_info'] = {
                'username': cd['username']
            }
            if User.objects.filter(username=cd['username']).exists():
                return redirect('AccountApp:login')
            code = randint(10000, 99999)
            print(code)
            OTP.objects.filter(username=cd['username']).delete()
            OTP.objects.create(username=cd['username'], code=code)
            if '@gmail' and '@email' in cd['username']:  # بعد از ثبت سامانه پیامک 
                send_mail(                               # and به or  تبدیل کنید
                    'Welcome to Shop',
                    f'Your OTP code is {code}',
                    'AshkanGhodrati01@gmail.com',
                    [cd['username']]
                )
            else:
                pass  #سامانه ارسال پیامک در اینجا بگذارید
            return redirect('AccountApp:verify_code')
        return render(request, 'AccountApp/register and login.html', {'form': form})


class VerifyOTP(View):
    def get(self, request):
        form = OTPVerifyForm()
        return render(request, 'AccountApp/login-otp.html', {'form': form})

    def post(self, request):
        form = OTPVerifyForm(request.POST)
        user_info = request.session['user_info']
        if not user_info:
            return redirect('AccountApp:register')
        username = user_info['username']
        if form.is_valid():
            cd = form.cleaned_data
            try:
                otp_instance = OTP.objects.get(username=username)
            except OTP.DoesNotExist:
                return redirect('AccountApp:register')
            if cd['code'] == otp_instance.code:
                user = User.objects.create(username=username)
                login(request, user)
                otp_instance.delete()
                return redirect('HomeApp:Home')
            form.add_error('code', 'کد معتبر نمیباشد')
            form.data = form.data.copy()
            form.data['code'] = ''   #در صورت اشتباه وارد کردن کد, همزمان با دادن اررور,  مغادیر داخل فیلد را پاک میکند
        return render(request, 'AccountApp/login-otp.html', {'form': form})


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'AccountApp/login-password.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        user_info = request.session['user_info']
        if not user_info:
            return redirect('AccountApp:register')
        username = user_info['username']
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=username, password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('HomeApp:Home')
            form.add_error('password', 'رمز عبور معتبر نمیباشد.')
        return render(request, 'AccountApp/login-password.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('HomeApp:Home')


class Forget(View):
    def get(self, request):
        form = RegisterForm()  #به دلیل مشابه بودن فیلد ها از فرم مشابه استفاده شده
        return render(request, 'AccountApp/forgot.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd['username']).exists():
                request.session['username_forget'] = {'username': cd['username']}
                code = randint(10000, 99999)
                print(code)
                OTP.objects.filter(username=cd['username']).delete()
                OTP.objects.create(username=cd['username'], code=code)
                return redirect('AccountApp:forget_otp')
            else:
                form.add_error('username', 'شماره موبایل یا ایمیل وارد شده وجود ندارد.')
        return render(request, 'AccountApp/forgot.html', {'form': form})


class ForgetOTPVerify(View):
    def get(self, request):
        form = OTPVerifyForm()
        return render(request, 'AccountApp/login-otp.html', {'form': form})   #به دلیل مشابه بودن ظاهر از تمپلت مشابه استفاده شده

    def post(self, request):
        form = OTPVerifyForm(request.POST)
        user_info = request.session['username_forget']
        if not user_info:
            return redirect('AccountApp:forget')
        username = user_info['username']
        if form.is_valid():
            cd = form.cleaned_data
            try:
                otp_instance = OTP.objects.get(username=username)
            except OTP.DoesNotExist:
                return redirect('AccountApp:forget')
            if cd['code'] == otp_instance.code:
                return redirect('AccountApp:reset_password')
            else:
                form.add_error('code', 'کد معتبر نمیباشد')
                form.data = form.data.copy()
                form.data['code'] = ''
        return render(request, 'AccountApp/login-otp.html', {'form': form})


class ResetPassword(View):
    def get(self, request):
        form = ResetForm()
        return render(request, 'AccountApp/forgot-reset.html', {'form': form})

    def post(self, request):
        form = ResetForm(request.POST)
        user_info = request.session['username_forget']
        if not user_info:
            return redirect('AccountApp:forget')
        username = user_info['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('AccountApp:forget')
        if form.is_valid():
            cd = form.cleaned_data
            password = cd['password']
            confirm_password = cd['confirm_password']
            if password == confirm_password:
                user.password = make_password(password)
                user.save()
                del request.session['username_forget']
                return redirect('AccountApp:register')
            else:
                form = ResetForm
        return render(request, 'AccountApp/forgot-reset.html', {'form': form})


class EnterOTP(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'AccountApp/forgot.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd['username']).exists():
                request.session['username_enter'] = {
                    'username': cd['username']
                }
                code = randint(10000, 99999)
                print(code)
                OTP.objects.filter(username=cd['username']).delete()
                OTP.objects.create(username=cd['username'], code=code)
                return redirect('AccountApp:enter_otp_verify')
            else:
                form.add_error('username', 'شماره موبایل یا ایمیل وارد شده وجود ندارد.')
        return render(request, 'AccountApp/forgot.html', {'form': form})


class EnterOTPVerify(View):
    def get(self, request):
        form = OTPVerifyForm()
        return render(request, 'AccountApp/login-otp.html', {'form': form})

    def post(self, request):
        form = OTPVerifyForm(request.POST)
        user_info = request.session['username_enter']
        if not user_info:
            return redirect('AccountApp:enter_otp')
        username = user_info['username']
        try:
            username = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('AccountApp:enter_otp')
        if form.is_valid():
            cd = form.cleaned_data
            try:
                otp_instance = OTP.objects.get(username=username)
            except OTP.DoesNotExist:
                return redirect('AccountApp:enter_otp')
            if cd['code'] == otp_instance.code:
                login(request, username)
                otp_instance.delete()
                del request.session['username_enter']
                return redirect('HomeApp:Home')
            else:
                form.add_error('code', 'کد معتبر نمیباشد')
                form.data = form.data.copy()
                form.data['code'] = ''
        return render(request, 'AccountApp/login-otp.html', {'form': form})


class ResendOTP(View):    # ارسال مجدد کد
    def post(self, request):
        username = request.session.get('user_info')['username']
        code = randint(10000, 99999)
        OTP.objects.filter(username=username).delete()
        OTP.objects.create(username=username, code=code)
        print(f'New Code {code}')
        return JsonResponse({"success": True, "message": "کد جدید ارسال شد."})
