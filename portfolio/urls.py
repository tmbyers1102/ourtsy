from django.urls import path
from portfolio.views import (
    ArtDashboardView,
    ArtCreateView,
    ArtDeleteView,
    ArtDetailView,
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
    path('art/create/', ArtCreateView.as_view(), name='art-create'),
    path('art/<str:slug>/', art_detail, name='art-detail'),
    path('art/<str:slug>/update/', art_update, name='art-update'),
    path('art/<str:slug>/delete/', ArtDeleteView.as_view(), name='art-delete'),
    path('art_dashboard/', ArtDashboardView.as_view(), name='art-dashboard'),
]