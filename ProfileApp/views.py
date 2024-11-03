from django.shortcuts import render
from django.views import View


class ProfileDashboard(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-dashboard.html')


class ProfileOrders(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-orders.html')


class ProfileFavorites(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-favorite.html')


class ProfileRecent(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-recent.html')


class ProfileNotification(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-notification.html')


class ProfileAddress(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-address.html')


class ProfileEdit(View):
    def get(self, request):
        return render(request, 'ProfileApp/profile-edit.html')