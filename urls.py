from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

'''#предыдущий url-адрес входа
    path('login/', views.user_login, name='login'),

    #url-адреса входа и выхода
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #url-адреса смены пароля
    path('password-change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    #url-адреса сброса пароля
    path('password-reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    это всё старое'''
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('wildberries_analitic', views.wildberries_analitic, name='wildberries_analitic'),
    path('ozon_analitic', views.ozon_analitic, name='ozon_analitic'),
    path("ozon_analitic/<str:name>", views.ozonGood),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)