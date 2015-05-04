from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/', include('lists.urls')),
    url(r'^accounts/', include('accounts.urls')),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
]
