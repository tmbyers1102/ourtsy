from django.core.mail import send_mail
from django.db.models import query
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView, FormView
from .models import Lead, Agent, User, UserProfile
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, UserUpdateForm, ArtistUpdateForm
from agents.mixins import OrganizerAndLoginRequiredMixin
from portfolio.mixins import ArtistAndLoginRequiredMixin


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = "dashboard/user_profile.html"
    queryset = UserProfile.objects.all()
    context_object_name = "profile_object"

    def get_context_data(self, **kwargs):
        dashboard_user = self.request.user.userprofile.slug
        dashboard_user_slug = str(dashboard_user).lower()
        context = {
            "dashboard_user": dashboard_user,
            "dashboard_user_slug": dashboard_user_slug,
        }
        return context


def user_settings(request, pk):
    dashboard_user = request.user.userprofile.slug
    dashboard_user_slug = str(dashboard_user).lower()
    if request.user.is_artist:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            a_form = ArtistUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.artist)
            if u_form.is_valid() and a_form.is_valid():
                u_form.save()
                a_form.save()
                messages.success(request,
                                f'Hey there,'
                                f' your account has been updated!')
                return redirect('portfolio:art-dashboard')
        else:
            u_form = UserUpdateForm(instance=request.user)
            a_form = ArtistUpdateForm(instance=request.user.artist)

        context = {
            "dashboard_user": dashboard_user,
            "dashboard_user_slug": dashboard_user_slug,
            'u_form': u_form,
            'a_form': a_form
        }
    else:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request,
                                f'Hey there,'
                                f' your account has been updated!')
                return redirect('user-profile', pk)
        else:
            u_form = UserUpdateForm(instance=request.user)

        context = {
            "dashboard_user": dashboard_user,
            "dashboard_user_slug": dashboard_user_slug,
            'u_form': u_form,
        }
    return render(request, "dashboard/user_profile.html", context)


class UserAnalyticsView(ArtistAndLoginRequiredMixin, DetailView):
    template_name = "dashboard/user_analytics.html"
    queryset = UserProfile.objects.all()
    context_object_name = "analytics_object"

    def get_context_data(self, **kwargs):
        dashboard_user = self.request.user.userprofile.slug
        dashboard_user_slug = str(dashboard_user).lower()
        context = {
            "dashboard_user": dashboard_user,
            "dashboard_user_slug": dashboard_user_slug,
        }
        return context


class FinancialSettingsView(LoginRequiredMixin, DetailView):
    template_name = "dashboard/financial_settings.html"
    queryset = UserProfile.objects.all()
    context_object_name = "financial_object"

    def get_context_data(self, **kwargs):
        dashboard_user = self.request.user.userprofile.slug
        dashboard_user_slug = str(dashboard_user).lower()
        context = {
            "dashboard_user": dashboard_user,
            "dashboard_user_slug": dashboard_user_slug,
        }
        return context


class LeadListView(LoginRequiredMixin, ListView):
    template_name = "lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "lead_list.html", context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for entire org
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "lead_detail.html", context)


class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        print('Receiving post request')
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "lead_create.html", context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for entire org
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        print('Receiving post request')
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "lead_update.html", context)


class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = "lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for entire org
        return Lead.objects.filter(organization=user.userprofile)


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")


class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView):
    template_name = "assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("portfolio:landing-page")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)




# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         print('Receiving post request')
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect("/leads")
    # context = {
    #     "form": form,
    #     "lead": lead
    # }
#     return render(request, "lead_update.html", context)


    # def lead_create(request):
        # form = LeadForm()
        # if request.method == "POST":
        #     print('Receiving post request')
        #     form = LeadForm(request.POST)
        #     if form.is_valid():
        #         first_name = form.cleaned_data['first_name']
        #         last_name = form.cleaned_data['last_name']
        #         age = form.cleaned_data['age']
        #         agent = Agent.objects.first()
        #         Lead.objects.create(
        #             first_name=first_name,
        #             last_name=last_name,
        #             age=age,
        #             agent=agent
        #         )
        #         return redirect("/leads")
    #     context = {
    #         "form": form
    #     }
    #     return render(request, "lead_create.html", context)