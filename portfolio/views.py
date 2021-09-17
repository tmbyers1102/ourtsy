from datetime import datetime, timedelta
from django.conf.urls import url
from django.db import models
from django.db.models import query
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.text import slugify
from django.utils.timesince import timesince
from .models import (
    ApprovalStatus,
    ArtGenre,
    ArtItem,
    ArtStatus,
    Artist,
    Portfolio,
    GenericStringTaggedItem,
    ArtMedium,
    ArtImage,
    ArtCommunity
)
from .forms import (
    ArtForm,
    ArtModelForm,
    CustomUserCreationForm,
    PostForm,
    ArtistForm,
    ArtUpdateModelForm,
    ArtReviewModelForm,
    ArtImageUpdateForm,
)
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from portfolio.mixins import ArtistAndLoginRequiredMixin
from .filters import ArtFilter, ArtTagFilter, ArtMediumFilter, ArtSubmissionsFilter

from .models import Post
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
import string
from urlparams.redirect import param_redirect


User = get_user_model()


def submitted(request):
    return render(request, "submitted.html")


def terms(request):
    return render(request, "terms.html")


def index(request):
    art = ArtItem.objects.filter(slug="the-new-cactus").first()
    artist = Artist.objects.filter(slug="tombyers").first()
    art_images = ArtImage.objects.all()
    art_images_count = ArtImage.objects.all().count()
    context = {
        "art": art,
        "artist": artist,
        "art_images": art_images,
        "art_images_count": art_images_count,
    }
    return render(request, "index.html", context)


class ReviewTableView(LoginRequiredMixin, generic.ListView):
    template_name = "dashboard/review_table.html"
    context_object_name = "art"
    queryset = ArtItem.objects.all()

    def get_context_data(self, **kwargs):
        dashboard_user = self.request.user.userprofile.slug
        dashboard_user_slug = str(dashboard_user).lower()
        order_by = self.request.GET.get('order_by', 'date_submitted')
        art = ArtItem.objects.all().order_by(order_by)
        art_count = art.count()
        not_yet_reviewed = ArtItem.objects.exclude(approval_status__name="Approved").count()
        rejected = ArtItem.objects.filter(approval_status__name="Rejected").count()
        approved_and_rejected_count = rejected \
            + ArtItem.objects.filter(approval_status__name="Approved").count()
        approval_avg = (ArtItem.objects.filter(approval_status__name="Approved").count() \
             / approved_and_rejected_count) * 100
        submissionsFilter = ArtSubmissionsFilter(self.request.GET, queryset=art)
        art = submissionsFilter.qs
        time_now = timezone.now
        threshold_24_hrs = datetime.now() - timedelta(days=1)
        print('threshold:')
        print(threshold_24_hrs)
        not_reviewed_over_24_count = ArtItem.objects\
            .exclude(approval_status__name="Approved")\
            .exclude(art_status__name="For Sale")\
            .filter(date_submitted__lt=threshold_24_hrs).count()
        not_reviewed_over_24_list = ArtItem.objects\
            .exclude(approval_status__name="Approved")\
            .exclude(art_status__name="For Sale")\
            .filter(date_submitted__lt=threshold_24_hrs)
        print(str('the not yet reviewed list:') + str(not_reviewed_over_24_list))
        # checks to see if recent submissions are passing 24hr w/o review and marking them for urgent review
        for x in not_reviewed_over_24_list:
            print('adding items to urgent review list')
            if x.urgent_review != True:
                print(str('updating urgent_review field to true... ') + str(x))
                x.urgent_review = True
                print('saved urgent_review field')
                x.save()
        # once those urgent review submissions are reviewed, we have to take them off the list
        approved_list = ArtItem.objects.filter(approval_status__name="Approved")
        for x in approved_list:
            print('removing items from urgent review list')
            if x.urgent_review == True:
                print(str('updating urgent_review field to false... ') + str(x))
                x.urgent_review = False
                print('saved urgent_review field')
                x.save()
      
        art_not_for_sale_yet = ArtItem.objects.exclude(art_status__name="For Sale")
        timesince_list = [timesince(x.date_submitted) for x in art_not_for_sale_yet]


        context = {
            "dashboard_user": dashboard_user,
            "dashboard_user_slug": dashboard_user_slug,
            "art": art,
            "not_yet_reviewed": not_yet_reviewed,
            "not_reviewed_over_24_count": not_reviewed_over_24_count,
            "not_reviewed_over_24_list": not_reviewed_over_24_list,
            "rejected": rejected,
            "approval_avg": approval_avg,
            "submissionsFilter": submissionsFilter,
            "time_now": time_now,
            "timesince_list": timesince_list,
            # "avg_wait_time": avg_wait_time,
            "art_count": art_count,
        }
        return context


# this is not being used
def art_review(request, slug):
    art = ArtItem.objects.get(slug=slug)
    form = ArtReviewModelForm(instance=art)
    tagsList = [x.tag for x in GenericStringTaggedItem.objects.filter(object_id=slug)]
    if request.method == "POST":
        print('POST Request on art review form')
        form = ArtReviewModelForm(request.POST, instance=art)
        if form.is_valid():
            form.save()
            return redirect("portfolio:art-dashboard")
    context = {
        "form": form,
        "art": art,
        "tagsList": tagsList,
    }
    return render(request, "dashboard/art_review.html", context)


def artist_list(request):
    artists = Artist.objects.all()
    context = {
        "artists": artists
    }
    return render(request, "artist_list.html", context)


def search_art(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = []
        artists_results= []
        # queries based on item's tags
        art_items = ArtItem.objects.filter(tags__name__icontains=searched)
        print('ART_ITEMS:')
        print(art_items)
        results.extend(art_items)
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
            Artist.objects.filter(art_genres__name__icontains=searched)
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
    showcase_art = ArtItem.objects.all().order_by('title')
    art = ArtItem.objects.filter(art_status__name='For Sale').filter(approval_status__name='Approved')
    myFilter = ArtFilter(request.GET, queryset=art)
    if request.GET:
        params = request
        return param_redirect(request, 'portfolio:art-list')
    context = {
        "artists": artists[0:6],
        "showcase_art": showcase_art[0:6],
        "myFilter": myFilter,
    }
    return render(request, "home/landing_1.html", context)


class ArtDashboardView(ArtistAndLoginRequiredMixin, generic.ListView):
    template_name = "dashboard/art_dashboard.html"
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
        artist_posts = Post.objects.filter(author=self.request.user).order_by('-published')
        artist_posts_count = Post.objects.filter(author=self.request.user).count()
        context = {
            "dashboard_user": dashboard_user,
            "dashboard_user_slug": dashboard_user_slug,
            "artist_items": artist_items,
            "artist_items_count": artist_items_count,
            "user_art_price_total": user_art_price_total,
            "avg_price_per_piece": avg_price_per_piece,
            "artist_posts": artist_posts,
            "artist_posts_count": artist_posts_count,
        }
        return context


# this one is in use
class ArtListView(generic.ListView):
    template_name = "art_list/art_list.html"
    model = ArtItem
    context_object_name = "art_items"
    paginate_by = 6
    ordering = ['-title']

    # def get_queryset(self):
    #     return ArtItem.objects.filter(art_status__name='For Sale').filter(approval_status__name='Approved')

    def get_context_data(self, **kwargs):
        context = super(ArtListView, self).get_context_data(**kwargs)
        # art = Paginator(ArtItem.objects.filter(art_status__name='For Sale').filter(approval_status__name='Approved'), self.paginate_by)
        art = ArtItem.objects.filter(art_status__name='For Sale').filter(approval_status__name='Approved')
        artists = Artist.objects.all()
        portfolios = Portfolio.objects.all()
        myFilter = ArtFilter(self.request.GET, queryset=art)
        tagFilter = ArtTagFilter(self.request.GET, queryset=art)
        mediumArtFilter = ArtMediumFilter(self.request.GET, queryset=art)
        mediumArtistFilter = ArtMediumFilter(self.request.GET, queryset=artists)
        art = myFilter.qs
        art_mediums = ArtMedium.objects.all()
        final_art = Paginator(art, 2)
        context = {
            "art": final_art,
            "portfolios": portfolios,
            "myFilter": myFilter,
            "art_mediums": art_mediums,
            "mediumArtFilter": mediumArtFilter,
            "mediumArtistFilter": mediumArtistFilter,
        }
        return context


def art_list(request):
    art = ArtItem.objects.filter(art_status__name='For Sale').filter(approval_status__name='Approved')
    # art_images = ArtImage.objects.filter(art_item=instance)
    artists = Artist.objects.all()
    portfolios = Portfolio.objects.all()
    myFilter = ArtFilter(request.GET, queryset=art)
    tagFilter = ArtTagFilter(request.GET, queryset=art)
    mediumArtFilter = ArtMediumFilter(request.GET, queryset=art)
    mediumArtistFilter = ArtMediumFilter(request.GET, queryset=artists)
    art = myFilter.qs
    art_mediums = ArtMedium.objects.all()
    art_communities = ArtCommunity.objects.all()
    art_genres = ArtGenre.objects.all()
    paginator = Paginator(art, 12) # how many items per page?
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "art": art,
        # "art_images": art_images,
        "portfolios": portfolios,
        "myFilter": myFilter,
        "art_mediums": art_mediums,
        "art_communities": art_communities,
        "art_genres": art_genres,
        "mediumArtFilter": mediumArtFilter,
        "mediumArtistFilter": mediumArtistFilter,
    }
    return render(request, "art_list/art_list.html", context)


def art_page(request):
    art = ArtItem.objects.all()
    context = {
        "art": art
    }
    return render(request, "art_page.html", context)


class PortfolioDetailView(generic.DetailView):
    model = ArtItem
    template_name = "portfolio/portfolio_detail.html"
    queryset = Portfolio.objects.all()
    context_object_name = "portfolio_object"

    # def get_queryset(self):
    #     print(str('queyset: ') + str(self.kwargs.get('pk')))
    #     return ArtItem.objects.filter(artist__slug='miltmiller')


def portfolio_detail(request, pk):
    portfolio = Portfolio.objects.get(slug=pk)
    artist = Artist.objects.get(slug=pk)
    portfolio_art = ArtItem.objects.filter(artist__slug=pk)
    artist_posts = Post.objects.filter(author__artist__pk=artist)
    context = {
        "portfolio": portfolio,
        "artist": artist,
        "portfolio_art": portfolio_art,
        "artist_posts": artist_posts,
    }
    return render(request, "portfolio/portfolio_detail.html", context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    user = get_object_or_404(User, username=post.author)
    authors_posts = Post.objects.filter(author = user).order_by('-published')[0:3]
    trending_posts = Post.objects.exclude(author = user)[0:3]

    context = {
        'post': post,
        'authors_posts': authors_posts,
        "trending_posts": trending_posts,
    }
    return render(request, "portfolio/post_detail.html", context)

class PostDetailView(generic.DetailView):
    template_name = "portfolio/post_detail.html"
    # queryset = Post.objects.filter(author = 3)
    context_object_name = "post"

    def get_object(self):
        return Post.objects.filter(slug = self.kwargs['slug'])[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors_posts = Post.objects.filter(slug = self)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "portfolio/post_create.html"
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, f'Success! Your post has been submitted for review. Until then, you may view it here in your dashboard.')
        return reverse("portfolio:art-dashboard")


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = "portfolio/post_update.html"
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        messages.success(self.request, f'Success! Your post has been updated and re-submitted for review. Until then, you may view it here in your dashboard.')
        return reverse("portfolio:art-dashboard")


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "portfolio/post_delete.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        messages.success(self.request, f'Success! Your post has been deleted.')
        return reverse("portfolio:art-dashboard")



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
    art_images = ArtImage.objects.filter(art_item=slug)
    tagsList = [x.tag for x in GenericStringTaggedItem.objects.filter(object_id=slug)]
    # for tag in ArtItem.tags.get_query_set():
    #     tagsList.append(tag.name)
    context = {
        "art": art,
        "tagsList": tagsList,
        "art_images": art_images,

    }
    return render(request, "art_detail/art_detail.html", context)


class ArtCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "art_create.html"
    form_class = ArtModelForm
    # success_url = reverse_lazy("portfolio:art-dashboard")
    # success_message = "Thing was created successfully."

    def get_success_url(self):
        messages.success(self.request, "created successfully")
        return reverse("portfolio:art-list")

    def form_valid(self, form):
        images = self.request.FILES.getlist('images')
        art_item = form.save(commit=False)
        # that 'artist' down there refers to the 'Artist' which the 'artist'
        # ForeignKey references on the ArtItem model in portfolio.models
        artist_slug = self.request.user.userprofile.slug
        art_item.artist = Artist.objects.get(slug=artist_slug)
        # art_item.art_status = str('Draft')
        # art_item.approval_status = str('Pending')
        art_item.save()
        return super(ArtCreateView, self).form_valid(form)

    # print('ADDING images to new ArtItem')
    # def add_the_photos(self, form):
    #     images = self.request.FILES.getlist('images')
    #     art_form = form
    #     for image in images:
    #         ArtImage.objects.create(
    #             art_item=art_form,
    #             image=image,
    #         )
    #         print('New image Created')
    #         ArtImage.save()
    #         print('New image Saved')
    #     return



# def art_create(request):
#     form = ArtForm()
#     if request.method == "POST":
#         print('Receiving post request')
#         form = ArtForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             artist = Artist.objects.first()
#             ArtItem.objects.create(
#                 title=title,
#                 artist=artist
#             )
#             return redirect("/")
#     context = {
#         "form": form
#     }
#     return render(request, "art_create.html", context)


def art_create(request):
    art_items = ArtItem.objects.all()
    form = ArtModelForm(request.POST)
    artist_instance = Artist.objects.filter(slug=request.user.userprofile.slug).first()

    if request.method == 'POST':
        data = request.POST
        print('data: ')
        print(data)
        # images = request.FILES.getlist('images')
        instance_mediums = request.POST.getlist('art_mediums')
        instance_communities = request.POST.getlist('art_communities')
        instance_genres = request.POST.getlist('art_genres')
        instance_auto_pub_value = request.POST.get('publish_after_approved')
        # get raw data
        raw_tags_data = request.POST.getlist('tags')
        print('raw_tags_data: ')
        print(raw_tags_data)
        # conv to a string
        raw_data_to_string = ' '.join(raw_tags_data)
        print('raw_data_to_string: ')
        print(raw_data_to_string)
        # conv string to actual list of strings
        tags_list_of_strings = list(raw_data_to_string.split(", "))
        print('tags_list_of_strings: ')
        print(tags_list_of_strings)

        # create the item
        if form.is_valid():
            art_item = ArtItem.objects.create(
                artist = artist_instance,
                title = data['title'],
                price = data['price'],
                art_story = data['art_story'],
            )
            art_item.art_mediums.set(instance_mediums)
            art_item.art_communities.set(instance_communities)
            art_item.art_genres.set(instance_genres)
            for x in tags_list_of_strings:
                art_item.tags.add(x)
            if instance_auto_pub_value:
                art_item.publish_after_approved = True
                art_item.save()
            # now create ArtImage model instances using the newly created ArtItem instance as the ArtImage's art_item field!
            images = request.FILES.getlist('images')
            print('Adding images for Item: ')
            print(art_item)
            print('Starting for loop: ')
            print(images)
            for image in images:
                photo = ArtImage.objects.create(
                    art_item=art_item,
                    image=image,
                )
                print('finished an image: ')
                print(image)
        
    
    context = {
        'art_items': art_items,
        'artist_instance': artist_instance,
        'form': form,
    }
    return render(request, 'art_create.html', context)


def art_new(request):
    art_items = ArtItem.objects.all()
    form = ArtModelForm(request.POST)
    artist_instance = Artist.objects.filter(slug=request.user.userprofile.slug).first()

    if request.method == 'POST':
        data = request.POST
        print('data: ')
        print(data)
        # images = request.FILES.getlist('images')
        instance_mediums = request.POST.getlist('art_mediums')
        instance_communities = request.POST.getlist('art_communities')
        instance_genres = request.POST.getlist('art_genres')
        instance_auto_pub_value = request.POST.get('publish_after_approved')
        # get raw data
        raw_tags_data = request.POST.getlist('tags')
        print('raw_tags_data: ')
        print(raw_tags_data)
        # conv to a string
        raw_data_to_string = ' '.join(raw_tags_data)
        print('raw_data_to_string: ')
        print(raw_data_to_string)
        # conv string to actual list of strings
        tags_list_of_strings = list(raw_data_to_string.split(", "))
        print('tags_list_of_strings: ')
        print(tags_list_of_strings)

        # create the item
        if form.is_valid():
            art_item = ArtItem.objects.create(
                artist = artist_instance,
                title = data['title'],
                price = data['price'],
                art_story = data['art_story'],
            )
            art_item.art_mediums.set(instance_mediums)
            art_item.art_communities.set(instance_communities)
            art_item.art_genres.set(instance_genres)
            for x in tags_list_of_strings:
                art_item.tags.add(x)
            if instance_auto_pub_value:
                art_item.publish_after_approved = True
                art_item.save()
            # now create ArtImage model instances using the newly created ArtItem instance as the ArtImage's art_item field!
            images = request.FILES.getlist('images')
            print('Adding images for Item: ')
            print(art_item)
            print('Starting for loop: ')
            print(images)
            for image in images:
                photo = ArtImage.objects.create(
                    art_item=art_item,
                    image=image,
                )
                print('finished an image: ')
                print(image)
            return redirect("portfolio:submitted")
    
    context = {
        'art_items': art_items,
        'artist_instance': artist_instance,
        'form': form,
    }
    return render(request, 'art_new_multi.html', context)


def artist_more(request, slug):
    art = ArtItem.objects.get(slug=slug)
    artist = art.artist.user
    artList = [x for x in ArtItem.objects.filter(artist__user=artist).filter(art_status__name='For Sale')]
    tagsList = [x.tag for x in GenericStringTaggedItem.objects.filter(object_id=slug)]
    art_images = ArtImage.objects.filter(art_item=slug)

    context = {
        "art": art,
        "tagsList": tagsList,
        "artList": artList,
        "art_images": art_images,
    }
    return render(request, "artist_more.html", context)


def art_images_update(request, slug):
    art_item_instance = ArtItem.objects.get(slug=slug)
    art_items = ArtItem.objects.all()
    form = ArtImageUpdateForm(request.POST)

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        art_item = ArtItem.objects.get(slug=slug)

        print('Adding images for Item: ')
        print(art_item)
        print('Starting for loop: ')
        print(images)
        for image in images:
            photo = ArtImage.objects.create(
                art_item=art_item,
                image=image,
            )
            print('finished an image: ')
            print(image)
        return redirect('portfolio:art-list')
    
    context = {
        'art_items': art_items,
        'art_item_instance': art_item_instance,
        'form': form,
    }
    return render(request, 'art_image_update.html', context)



# def art_images_update(request, slug):
#     art_item_instance = ArtItem.objects.get(slug=slug)
#     art_images = ArtImage.objects.filter(art_item=slug)
#     images = request.FILES.getlist('images')
#     print('IMAGES:')
#     print(images)
#     for image in images:
#         print(image)
#         print('made it tofor loop')
#         if request.method == 'POST':
#             print('made it past the if POST')
#             art_image_form = ArtImageUpdateForm(request.POST, instance=[1])
#             print(str('art_image_form instance: ') + str(art_image_form) )
#             if art_image_form.is_valid():
#                 print('made it past the is_valid')
#                 print(art_image_form.errors)
#                 ArtImage.objects.create(
#                         art_item=art_item_instance,
#                         image=image,
#                     )
#                 print('made it past create part --not saved yet')
#                 art_image_form.save()
#                 print('made it past the SAVED part')
#                 return redirect("portfolio:art-detail", slug=slug)
#     context = {
#         'art_item_instance': art_item_instance,
#         # "art_image_form": art_image_form,
#         "art_images": art_images,
#     }
#     return render(request, 'art_image_update.html', context)


# def art_images_update(request, slug):
#     art = ArtItem.objects.get(slug=slug)
#     form = ArtImageUpdateForm(instance=art)
#     tagsList = [x.tag for x in GenericStringTaggedItem.objects.filter(object_id=slug)]
#     art_images = ArtImage.objects.filter(art_item=slug)
#     if request.method == "POST":
#         print('> Receiving post request -- ART images update')
#         form = ArtImageUpdateForm(request.POST or None, instance=art)
#         if form.is_valid():
#             print('>> form is valid, going into if statements')
#             # lets add any new images
#             print('ADDING images to existing ArtItem')
#             images = request.FILES.getlist('images')
#             art_slug = ArtItem.objects.filter(slug=slug).first()
#             print(art_slug)
#             for image in images:
#                 ArtImage.objects.create(
#                     art_item=art_slug,
#                     image=image,
#                 )
#                 print('New image Created')
#                 print('New image Saved')
#                 # end of adding new images
#                 form.save()
#                 messages.success(request, "Success! Art Images Added!")
#                 return redirect("portfolio:art-detail", slug=slug)
#         else:
#             messages.error(request, "error! form not valid!")
#             print('Form valid errors:')
#             print(form.errors)
#             return redirect("portfolio:art-detail", slug=slug)
#     context = {
#         "form": form,
#         "art": art,
#         "tagsList": tagsList,
#         "art_images": art_images,
#     }
#     return render(request, "art_image_update.html", context)


def art_update(request, slug):
    art = ArtItem.objects.get(slug=slug)
    form = ArtUpdateModelForm(instance=art)
    tagsList = [x.tag for x in GenericStringTaggedItem.objects.filter(object_id=slug)]
    art_images = ArtImage.objects.filter(art_item=slug)

    if request.method == "POST":
        print('> Receiving post request -- ART UPDATE')
        form = ArtUpdateModelForm(request.POST or None, instance=art)
        if form.is_valid():
            print('>> form is valid, going into if statements')
            # lets add any new images
            print('ADDING images to existing ArtItem')
            images = request.FILES.getlist('images')
            art_slug = form.cleaned_data["slug"]
            for image in images:
                ArtImage.objects.create(
                    art_item=art,
                    image=image,
                )
                print('New image Created')
                print('New image Saved')
            # end of adding new images
            if art.publish_after_approved:
                print('>>> wants to publish after approved')
                if art.approval_status.name == 'Approved':
                    print('>>>> the items approval status is approved')
                    if art.art_status.name != 'For Sale':
                        print('>>>>> the art_status for this item is not For Sale so we will switch it to that')
                        art.art_status = ArtStatus.objects.filter()[1]
                        form.save()
                        messages.success(request, "Success! Art Item Updated!")
                        return redirect("portfolio:art-detail", slug=slug)
                    else:
                        print('<<<<< the art_status WAS for sale so passing')
                        form.save()
                        messages.success(request, "Success! Art Item Updated!")
                        return redirect("portfolio:art-detail", slug=slug)
                else:
                    print('<<<< the items approval status is NOT approved')
                    form.save()
                    messages.success(request, "Success! Art Item Updated!")
                    return redirect("portfolio:art-detail", slug=slug)
            else:
                print('<<< does NOT want to publish after approved')
                form.save()
                messages.success(request, "Success! Art Item Updated!")
                return redirect("portfolio:art-detail", slug=slug)
        else:
            print('<< This is an ART UPDATE POST request but not a valid form')
            print(form.errors)
            messages.error(request, "This is an ART UPDATE POST request but not a valid form")
    else:
        print('< This is not a POST request -- art update')
    context = {
        "form": form,
        "art": art,
        "tagsList": tagsList,
        "art_images": art_images,
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