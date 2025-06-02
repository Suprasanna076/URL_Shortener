from django.contrib import admin
from django.urls import path,include
from . import views 

urlpatterns = [
   path('hello',views.hello_world),
   path('',views.home_page),
   # path('task',views.task),
   path('all-analytics',views.all_analytics,name='all_analytics'),
   path('analytics/<slug:short_url>', views.analytics, name='analytics_detail'),

   path('<slug:short_url>',views.redirect_url,name='redirect_url')
   
]

#localhost:8000/hello
