from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
    path('brands/', include('brands.urls')),
    path('influencers/', include('influencers.urls')),
    path('campaigns/', include('campaigns.urls')),
    path('messaging/', include('messaging.urls')),
    path('notifications/', include('notifications.urls')),
    path('reviews/', include('reviews.urls')),
    path('reports/', include('reports.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('payments/', include('payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)