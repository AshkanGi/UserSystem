from django.shortcuts import redirect
from django.urls import reverse

"""
بعد از لاگین به این صفحات دسترسی ندارین
"""


class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.restricted_urls = [
            reverse('AccountApp:register'),
            reverse('AccountApp:verify_code'),
            reverse('AccountApp:login'),
            reverse('AccountApp:forget'),
            reverse('AccountApp:forget_otp'),
            reverse('AccountApp:reset_password'),
            reverse('AccountApp:enter_otp'),
            reverse('AccountApp:enter_otp_verify'),
        ]

    def __call__(self, request):
        if request.user.is_authenticated and request.path in self.restricted_urls:
            return redirect('HomeApp:Home')
        return self.get_response(request)