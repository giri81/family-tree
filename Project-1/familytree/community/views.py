from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Community, CommunityMember
from . import models


class CreateCommunity(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Community


class SingleCommunity(generic.DetailView):
    model = Community


class ListCommunity(generic.ListView):
    model = Community


class JoinCommunity(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('communities:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        community = get_object_or_404(Community, slug=self.kwargs.get('slug'))

        try:
            CommunityMember.objects.create(user=self.request.user, community=community)

        except IntegrityError:
            messages.warning(self.request, ("Warning, already a member of {}".format(community.name)))

        else:
            messages.success(self.request, "You are now a member of the {} group.".format(community.name))

        return super().get(request, *args, **kwargs)


class LeaveCommunity(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('communities:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.CommunityMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.CommunityMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this community because you aren't in it."
            )

        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this community."
            )
        return super().get(request, *args, **kwargs)
