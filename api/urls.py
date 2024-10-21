from django.urls import path

from api import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get', views.get, name='get'),
    path('timetable', views.timetable_view, name='timetable'),

]
