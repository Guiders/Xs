from django.conf.urls import url, include
from django.views.static import serve
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls
from users.views import SmsCodeViewset, UserViewset
import xadmin
from XServer.settings import MEDIA_ROOT

router = DefaultRouter()
router.register(r'users', UserViewset, base_name="users")
router.register(r'codes', SmsCodeViewset, base_name="codes")

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'docs/', include_docs_urls(title="xshop")),

    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt的token认证模式
    url(r'^login/', obtain_jwt_token),
]
