from django.shortcuts import render
from django.views.generic import DetailView

from cabinet.models import User


def get_profile(request):
    return render(request, template_name='cabinet/profile.html')


class ProfileDetail(DetailView):
    model = User
    template_name = 'cabinet/profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'id'
