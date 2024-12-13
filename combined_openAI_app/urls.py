from django.urls import path
from . import views
from demo.views import demo_home
from chatbot.views import chat_home
from combined_openAI_app.views import PII, SSC, upload_document2, analyze_sensitivity
urlpatterns = [
    path('', views.home, name='home'),  
    path('banner-image/', views.banner_image, name='banner-image'),
    path('demo_home/', demo_home, name = 'demo_home'),
    path('chat_home/', chat_home, name = 'chat_home'),
    path('PII/', PII, name = 'PII'),
    path('SSC/', SSC, name = 'SSC'),
    path('upload_document2/', upload_document2, name = 'upload_document2'),
    path('analyze_sensitivity/', analyze_sensitivity, name = 'analyze_sensitivity'),




]
