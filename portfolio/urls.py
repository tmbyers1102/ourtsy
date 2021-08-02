from django.urls import path
from portfolio.views import (
    ArtDashboardView,
    ArtCreateView,
    art_list,
    art_create,
    art_detail,
    art_update,
    portfolio_detail,
    art_delete,
    landing_page,
    LandingPageView
)

app_name = "portfolio"

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing-page'),
    path('art/', art_list, name='art-list'),
    path('art/<int:pk>/', art_detail, name='art-detail'),
    path('art/<int:pk>/update/', art_update, name='art-update'),
    path('art/<int:pk>/delete/', art_delete, name='art-delete'),
    path('art/create/', ArtCreateView.as_view(), name='art-create'),
    path('<int:pk>/', portfolio_detail, name='portfolio-detail'),
    path('art_dashboard/', ArtDashboardView.as_view(), name='art-dashboard'),
]