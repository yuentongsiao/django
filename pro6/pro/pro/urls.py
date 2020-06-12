"""pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
# from learn import views as learn_views
from learn import urls as learn_urls

from django.conf.urls.static import static # 新加入
from django.conf import settings # 新加入

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',include((learn_urls,'learn'),namespace='learn')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
