from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class ArtistAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organizer."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_artist:
            return redirect("portfolio:landing-page")
        return super().dispatch(request, *args, **kwargs)