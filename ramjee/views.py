from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Manushya
from .models import Harkare
from utils import send_email, helper
from harkare import settings

@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def upload_harkara(request):
    context = {}
    if request.method == 'POST':
        postdata = request.FILES
        harkara_list = postdata.getlist('harkara[]')

        email = request.user.email
        manushya = Manushya.objects.filter(email=email).first()

        for harkara in harkara_list:
            harkara_obj = Harkare.objects.create(manushya=manushya, name=harkara.name)
            minio_url = helper.handle_uploaded_file(harkara, rename=harkara_obj.id)

        url = reverse('ramjee:harkare')

        return HttpResponseRedirect(url)

    context['page_title'] = 'Upload Harkara'

    return render(request, 'ramjee/upload.html', context)

@login_required
def list_harkare(request):
    context = {}
    return render(request, 'ramjee/harkare.html', context)
