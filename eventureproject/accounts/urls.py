from django.urls import path
from . import views  as accountsViews

urlpatterns = [
    path('', accountsViews.home, name='home'),
    path('signup/', accountsViews.signupaccount, name='signupaccount'),
    path('login/', accountsViews.loginaccount, name='loginaccount'),
    path('logout/', accountsViews.signoutaccount, name='signoutaccount'),
]
