from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.text import slugify
from .models import ArtItem, Artist, Portfolio, GenericStringTaggedItem
from .forms import ArtForm, ArtModelForm, CustomUserCreationForm, PostForm, ArtistForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from portfolio.mixins import ArtistAndLoginRequiredMixin
from .filters import ArtFilter, ArtTagFilter

from .models import Post
from django.contrib.auth import get_user_model


User = get_user_model()


def search_art(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = []
        artists_results= []
        # queries based on item's tags
        art_items = ArtItem.objects.filter(tags__name__icontains=searched)
        print('ART_ITEMS:')
        print(art_items)
        titles = ArtItem.objects.filter(title__icontains=searched)
        print('TITLES:')
        print(titles)
        for x in titles:
            if x in results:
                pass
            else:
                results.extend(titles)
        # queries based on item's related artist
        artists_items = \
            ArtItem.objects.filter(artist__user__username__icontains=searched) or \
            ArtItem.objects.filter(artist__slug__icontains=searched) or \
            ArtItem.objects.filter(artist__user__first_name__icontains=searched) or \
            ArtItem.objects.filter(artist__user__last_name__icontains=searched)
        print('ARTISTS_ITEMS:')
        print(artists_items)
        for x in artists_items:
            if x in results:
                pass
            else:
                results.extend(artists_items)
        if not searched:
            results = ArtItem.objects.all()
        artist_list = \
            Artist.objects.filter(user__username__icontains=searched) or \
            Artist.objects.filter(user__first_name__icontains=searched) or \
            Artist.objects.filter(user__last_name__icontains=searched)
            # Artist.objects.filter(user__slug__icontains=searched)
        print('ARTIST_LIST:')
        print(artist_list)
        artists_results.extend(artist_list)
        artist_genre_list = \
            Artist.objects.filter(genres__name__icontains=searched)
        print('ARTIST_GENRE_LIST:')
        print(artist_genre_list)
        for y in artist_genre_list:
            if y in artists_results:
                pass
            else:
                artists_results.extend(artist_genre_list)
        # query the art_items that will be showm and show all their respective artists
        artists_from_items_list = []
        for x in results:
            get_the_artist = Artist.objects.filter(slug=x.artist)
            if get_the_artist[0] in artists_results:
                pass
            else:
                artists_results.extend(get_the_artist)
        context = {
            'searched': searched,
            'art_items': art_items,
            'results': results,
            'artists_results': artists_results,
            'artists_from_items_list': artists_from_items_list,
        }
        return render(request, 'search_art.html', context)
    else:
        return reverse(request, 'portfolio:art-list')



class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing_1.html"


def landing_page(request):
    artists = Artist.objects.all().order_by('-user_id')
    context = {
        "artists": artists[0:6]
    }
    return render(request, "landing_1.html", context)


class ArtDashboardView(ArtistAndLoginRequiredMixin, generic.ListView):
    template_name = "art_dashboard.html"
    context_object_name = "art_items"

    def get_queryset(self):
        artist = self.request.user.userprofile.slug
        return ArtItem.objects.filter(artist=artist)

    def get_context_data(self, **kwargs):
        dashboard_user = self.request.user.userprofile.slug
        dashboard_user_slug = str(dashboard_user).lower()
        artist_items = ArtItem.objects.filter(artist=dashboard_user)
        artist_items_count = ArtItem.objects.filter(artist=dashboard_user).count()
        user_art_price_total = sum([x.price for x in artist_items])
        if user_art_price_total <= 1 or artist_items_count <= 1:
            avg_price_per_piece = str('NA')
        else:
            avg_price_per_piece = float(user_art_price_total/artist_items_count)
        context = {
            "dashboard_user": dashboard_user,
            "dashboard_user_slug": dashboard_user_slug,
            "artist_items": artist_items,
            "artist_items_count": artist_items_count,
            "user_art_price_total": user_art_price_total,
            "avg_price_per_piece": avg_price_per_piece,
        }
        return context


class ArtListView(generic.ListView):
    template_name = "art_list.html"
    context_object_name = "art_items"

    def get_queryset(self):
        return ArtItem.objects.all()

    def get_context_data(self, **kwargs):
        art = ArtItem.objects.all()
        portfolios = Portfolio.objects.all()
        context = {
            "art": art,
            "portfolios": portfolios,
        }
        return context


def art_list(request):
    art = ArtItem.objects.all()
    portfolios = Portfolio.objects.all()
    myFilter = ArtFilter(request.GET, queryset=art)
    tagFilter = ArtTagFilter(request.GET, queryset=art)
    art = myFilter.qs
    context = {
        "art": art,
        "portfolios": portfolios,
        "myFilter": myFilter,
    }
    return render(request, "art_list.html", context)


def art_page(request):
    art = ArtItem.objects.all()
    context = {
        "art": art
    }
    return render(request, "art_page.html", context)


class PortfolioDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "portfolio_detail.html"
    queryset = Portfolio.objects.all()
    context_object_name = "portfolio_object"


def portfolio_detail(request, pk):
    portfolio = Portfolio.objects.get(slug=pk)
    context = {
        "portfolio": portfolio
    }
    return render(request, "portfolio_detail.html", context)


class ArtDetailView(generic.DetailView):
    template_name = "art_detail.html"
    queryset = ArtItem.objects.all()
    context_object_name = "art"

    def get_context_data(self, **kwargs):
        art_user = self.request.user.userprofile.slug
        art_user_slug = str(art_user).lower()
        context = {
            "art_user": art_user,
            "art_user_slug": art_user_slug,
        }
        return context


def art_detail(request, slug):
    art = ArtItem.objects.get(slug=slug)
    tagsList = [x.tag for x in GenericStringTaggedItem.objects.filter(object_id=slug)]
    # for tag in ArtItem.tags.get_query_set():
    #     tagsList.append(tag.name)
    context = {
        "art": art,
        "tagsList": tagsList

    }
    return render(request, "art_detail.html", context)


class ArtCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "art_create.html"
    form_class = ArtModelForm

    def get_success_url(self):
        return reverse("portfolio:art-dashboard")

    def form_valid(self, form):
        art_item = form.save(commit=False)
        # that 'artist' down there refers to the 'Artist' which the 'artist'
        # ForeignKey references on the ArtItem model in portfolio.models
        artist_slug = self.request.user.userprofile.slug
        art_item.artist = Artist.objects.get(slug=artist_slug)
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


def art_update(request, slug):
    art = ArtItem.objects.get(slug=slug)
    form = ArtModelForm(instance=art)
    tagsList = [x.tag for x in GenericStringTaggedItem.objects.filter(object_id=slug)]
    if request.method == "POST":
        print('Receiving post request')
        form = ArtModelForm(request.POST, instance=art)
        if form.is_valid():
            form.save()
            return redirect("portfolio:art-dashboard")
    context = {
        "form": form,
        "art": art,
        "tagsList": tagsList
    }
    return render(request, "art_update.html", context)


class ArtDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "art_delete.html"
    queryset = ArtItem.objects.all()

    def get_success_url(self):
        return reverse("portfolio:art-dashboard")


def art_delete(request, slug):
    art = ArtItem.objects.get(slug=slug)
    art.delete()
    return redirect("/")


def post_create(request):
    form = PostForm()
    posts = Post.objects.all()
    if request.method == "POST":
        print('Receiving post POST request')
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            # tags = form.cleaned_data['tags']
            Post.objects.create(
                title=title,
                description=description,
                # tags=tags,
            )
            return redirect("portfolio:post-list")
    context = {
        "form": form,
        "posts": posts,
    }
    return render(request, "post_create.html", context)


def post_list(request):
    posts = Post.objects.all()
    context = {
        "posts": posts,
    }
    return render(request, "post_list.html", context)


def home_view(request):
    posts = Post.objects.all()
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        form.save_m2m()
    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
    }
    return render(request, 'home.html', context)


def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post':post,
    }
    return render(request, 'detail.html', context)


def art_search(request, slug):
    tag = str(slug)
    art_items = ArtItem.objects.filter(tags__name__icontains=slug)
    context = {
        'art_items':art_items,
        'tag': tag
    }
    return render(request, 'tag.html', context)





def artist_create(request):
    form = ArtistForm()
    if request.method == "POST":
        print('Receiving post request -- ArtistForm')
        form = ArtistForm(request.POST)
        if form.is_valid():
            user = request.user
            Artist.objects.create(
                user=user,
            )
            return redirect("/")
    context = {
        "form": form
    }
    return render(request, "artist_create.html", context)