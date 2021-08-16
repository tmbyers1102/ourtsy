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
    # portfolio_detail,
    art_delete,
    landing_page,
    LandingPageView,
    home_view,
    detail_view,
    art_search,
    post_create,
    post_list,
    artist_create,
    ArtListView,
    search_art,
    artist_list,
    test
)

app_name = "portfolio"

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('art/', art_list, name='art-list'),
    path('artists/', artist_list, name='artist-list'),
    path('post_list/', post_list, name='post-list'),
    path('post/', home_view, name='home'),
    path('posts/', post_create, name='post-create'),
    path('post/<slug:slug>/', detail_view, name='detail'),
    path('tag/<str:slug>/', art_search, name='art-search'),
    path('art/create/', ArtCreateView.as_view(), name='art-create'),
    path('art/<str:slug>/', art_detail, name='art-detail'),
    path('art/<str:slug>/update/', art_update, name='art-update'),
    path('art/<str:slug>/delete/', ArtDeleteView.as_view(), name='art-delete'),
    path('art_dashboard/', ArtDashboardView.as_view(), name='art-dashboard'),
    path('artist/create/', artist_create, name='artist-create'),
    path('search_art/', search_art, name='search-art'),
    path('test/', test, name='test'),
]