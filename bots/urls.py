from django.contrib import admin
from django.urls import path, include
from altwhales import views
from altfishbot import urls as altfishbot_urls
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('altfishbot/', include(altfishbot_urls)),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.index, name='index'),
]