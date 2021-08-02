from django.shortcuts import render, redirect, reverse
from .models import ArtItem, Artist, Portfolio
from .forms import ArtForm, ArtModelForm, CustomUserCreationForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing_3.html"


def landing_page(request):
    return render(request, "landing.html")


class ArtDashboardView(LoginRequiredMixin, generic.ListView):
    template_name = "art_dashboard.html"
    context_object_name = "art_items"

    def get_queryset(self):
        artist = self.request.user.artist
        return ArtItem.objects.filter(artist=artist)


def art_list(request):
    art = ArtItem.objects.all()
    portfolios = Portfolio.objects.all()
    context = {
        "art": art,
        "portfolios": portfolios,
    }
    return render(request, "art_list.html", context)

def art_page(request):
    art = ArtItem.objects.all()
    context = {
        "art": art
    }
    return render(request, "art_page.html", context)


def portfolio_detail(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    context = {
        "portfolio": portfolio
    }
    return render(request, "portfolio_detail.html", context)


def art_detail(request, pk):
    art = ArtItem.objects.get(id=pk)
    context = {
        "art": art
    }
    return render(request, "art_detail.html", context)


class ArtCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "art_create.html"
    form_class = ArtModelForm

    def get_success_url(self):
        return reverse("portfolio:art-list")

    def form_valid(self, form):
        art_item = form.save(commit=False)
        # that 'artist' down there refers to the 'Artist' which the 'artist'
        # ForeignKey references on the ArtItem model in portfolio.models
        art_item.artist = self.request.user.artist
        art_item.save()
        return super(ArtCreateView, self).form_valid(form)

def art_create(request):
    form = ArtForm()
    if request.method == "POST":
        print('Receiving post request')
        form = ArtForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            artist = Artist.objects.first()
            ArtItem.objects.create(
                title=title,
                artist=artist
            )
            return redirect("/")
    context = {
        "form": form
    }
    return render(request, "art_create.html", context)

def art_update(request, pk):
    art = ArtItem.objects.get(id=pk)
    form = ArtModelForm(instance=art)
    if request.method == "POST":
        print('Receiving post request')
        form = ArtModelForm(request.POST, instance=art)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {
        "form": form,
        "art": art
    }
    return render(request, "art_update.html", context)

def art_delete(request, pk):
    art = ArtItem.objects.get(id=pk)
    art.delete()
    return redirect("/")
