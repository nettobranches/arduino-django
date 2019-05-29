from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('init/<str:port>', views.init, name='init'),
    path('setval/<str:tipo>/<str:idx>/<str:mode>/<str:value>', views.set_value, name='set_value'),
    path('get_analog_val/<str:idx>/', views.getAnalogVal, name='getAnalogVal'),
    path('get_digital_val/<str:idx>/', views.getDigitalVal, name='getDigitalVal'),
    path('start_analog/<str:idx>/<str:mode>', views.startAnalogPin, name='startAnalogPin'),
    path('start_digital/<str:idx>/<str:mode>', views.startDigitalPin, name='startDigitalPin'),
    path('test/read', views.test_read, name='test_read'),

    path('start_servo/', views.startServo, name='startServo'),
    path('move_servo/<str:deg>', views.moveServo, name='moveServo'),
]