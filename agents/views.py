import random
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from leads.models import UserProfile
from .mixins import OrganizerAndLoginRequiredMixin
from agents.forms import User


# LIST
class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = 'agent_list.html'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


# CREATE
class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    model = User
    template_name = 'agent_create.html'
    from_class = AgentModelForm
    fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)

        try:
            user_profile = self.request.user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=self.request.user)

        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0, 100)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM. Please come login to start working.",
            from_email="iliadi.lo.lolita@gmail.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


# DETAIL
class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


# UPDATE
class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    model = Agent
    template_name = 'agent_update.html'
    from_class = AgentModelForm
    fields = (
        'user',
    )

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


# DELETE
class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agent_delete.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
