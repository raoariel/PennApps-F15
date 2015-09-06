from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register$', views.register, name='register'),
    url(r'^get_messages$', views.get_messages, name='get_messages'),
]
