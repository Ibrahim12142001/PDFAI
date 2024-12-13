from django.urls import path
from demo import views

urlpatterns = [
    path('demo_home', views.demo_home, name='demo_home'),  # Home page
    path('upload/', views.OpenAIView.as_view(), name='upload'),  # Upload page, using the existing OpenAIView
    # Uncomment the next line when you're ready to implement the export functionality
    # path('openai/export/', views.OpenAIExportView.as_view(), name='export_openai_data'),
]
