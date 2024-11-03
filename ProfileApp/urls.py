from django.urls import path
from . import views


app_name = 'ProfileApp'
urlpatterns = [
    path('', views.ProfileDashboard.as_view(), name='profile_dashboard'),
    path('orders', views.ProfileOrders.as_view(), name='profile_orders'),
    path('favorite', views.ProfileFavorites.as_view(), name='profile_favorite'),
    path('recent', views.ProfileRecent.as_view(), name='profile_recent'),
    path('notification', views.ProfileNotification.as_view(), name='profile_notification'),
    path('address', views.ProfileAddress.as_view(), name='profile_address'),
    path('edit', views.ProfileEdit.as_view(), name='profile_edit'),
]