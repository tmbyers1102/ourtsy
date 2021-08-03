from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from .models import Lead, Agent, User, UserProfile
from .forms import LeadForm, LeadModelForm
from agents.mixins import OrganizerAndLoginRequiredMixin



class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = "user_profile.html"
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


class UserAnalyticsView(LoginRequiredMixin, DetailView):
    template_name = "user_analytics.html"
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
    template_name = "financial_settings.html"
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
    queryset = Lead.objects.all()
    context_object_name = "leads"


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "lead_list.html", context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


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
    queryset = Lead.objects.all()
    form_class = LeadModelForm

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
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

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