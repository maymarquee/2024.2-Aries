from django.contrib import admin
from django.urls import path, include
from Users.views import login, register, recoverAccount, redefinePassword
from guest.views import index, competition, admission
from members.views import sidebar, home

urlpatterns = [

    path('admin/', admin.site.urls),

    # Users
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('account_recovery/', recoverAccount, name='recoverAccount'),
    path('redefine_password/<str:username>/<str:token>', redefinePassword, name="redefinePassword"),

    # guest
    path('', index, name="index"),
    path('competition/', competition, name="competition"),
    path('admission/', admission, name="admission"),

    # report
    path('report/', include('report.urls')),

    # members
    path('sidebar/', sidebar,name="sidebar"),
    path('home/', home, name="home"),

    # stock
    
]
