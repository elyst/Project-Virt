from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', include("LandingPage.urls")),
    url(r'^VMManager/', include("VMManager.urls")),
    url(r'^login/', include("Login.urls")),
    url(r'^dashboard/', include("Dashboard.urls")),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)