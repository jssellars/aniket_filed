"""adpreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from facebook_assets import views as facebook_assets_views
from staticpreview import views as static_preview_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate-preview/', static_preview_views.GenerateAdPreview),
    path('<str:business_owner_facebook_id>/ad-images/<str:ad_account_id>', facebook_assets_views.GetAdImages),
    path('<str:business_owner_facebook_id>/ad-videos/<str:ad_account_id>', facebook_assets_views.GetAdVideos),
    path('<str:business_owner_facebook_id>/page-posts/<str:page_facebook_id>',
         facebook_assets_views.GetPagePostsMinimal)
]
