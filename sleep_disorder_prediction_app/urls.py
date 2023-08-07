from capstone_project.urls import path
from . import views

urlpatterns=[
    path('',views.form,name='form'),
    path('result',views.predictor,name='result')
]