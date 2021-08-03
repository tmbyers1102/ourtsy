from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from portfolio.views import SignupView, portfolio_detail
from leads.views import UserAnalyticsView, UserProfileView, FinancialSettingsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls', namespace="leads")),
    path('agents/', include('agents.urls', namespace="agents")),
    path('', include('portfolio.urls', namespace="portfolio")),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<str:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('user/analytics/<str:pk>/', UserAnalyticsView.as_view(), name='user-analytics'),
    path('user/financial/<str:pk>/', FinancialSettingsView.as_view(), name='financial-settings'),
    path('<str:pk>/', portfolio_detail, name='portfolio-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)