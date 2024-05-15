from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

# pip install django-braces
from braces.views import SelectRelatedMixin

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()


class MemberList(SelectRelatedMixin, generic.ListView):
    model = models.Member
    select_related = ("user", "community")


class UserMember(generic.ListView):
    model = models.Member
    template_name = "member/user_member_list.html"

    def get_queryset(self):
        try:
            self.member_user = User.objects.prefetch_related("member").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.member_user.member.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["member_user"] = self.member_user
        return context


class MemberDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Member
    select_related = ("user", "community")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreateMember(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','community')
    model = models.Member

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteMember(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Member
    select_related = ("user", "community")
    success_url = reverse_lazy("member:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Member Deleted")
        return super().delete(*args, **kwargs)
