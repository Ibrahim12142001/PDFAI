from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('combined_openAI_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),
    path('', include('demo.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)