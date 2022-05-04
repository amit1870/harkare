from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Manushya, HexString
from utils import send_email, helper
from harkare import settings


@csrf_protect
@require_http_methods(["GET", "POST"])
def register(request):
    context = {}
    if request.method == 'POST':
        postdata = request.POST.copy()
        user_name = postdata.get('username','')
        email = postdata.get('email','')
        pitaji = postdata.get('pitaji', '')
        mataji = postdata.get('mataji', '')
        gaon = postdata.get('gaon', '')
        viradari = postdata.get('viradari', '')
        password = postdata.get('inputPassword1','')

        if user_name == '':
            user_name = 'SiyaRam'

        if pitaji == '':
            pitaji = 'Dasharath'

        if mataji == '':
            mataji == 'Kaushlya'

        if gaon == '':
            gaon = 'Harkarapur'

        if viradari == '':
            viradari = 'SiyaRam'

        manushya = get_user_model().objects.filter(email=email).first()

        if not manushya:
            manushya = Manushya.objects.create(email=email, user_name=user_name, pitaji=pitaji, mataji=mataji, gaon=gaon, viradari=viradari)
            manushya.set_password(password)
            manushya.save()
            hex_string = HexString.objects.create(code=helper.generate_hex_string(), manushya=manushya)
            hex_code = hex_string.code

            if manushya:
                service = send_email.create_service(
                    settings.GOOGLE_API['token_path'],
                    settings.GOOGLE_API['pickle_path'],
                    settings.GOOGLE_API['name'],
                    settings.GOOGLE_API['version'],
                    settings.GOOGLE_API['scope']
                )
                message_list = []
                EMAIL = {
                    'from': 'amitxvf@gmail.com',
                    'to': email + ",amitxvf@gmail.com",
                    'subject': 'Welcome to Harkare...',
                    'content': f'Dear <b>{user_name}</b>, Thanks for your registration at Harkare.<br/>Click https://harkare.herokuapp.com/activate/{hex_code}.'
                }
                message = send_email.create_plain_html_message(EMAIL['from'],
                            EMAIL['to'],
                            EMAIL['subject'],
                            EMAIL['content'],
                            html=True)
                message_list.append(message)

                message_response = send_email.send_message(service, EMAIL['from'], message)

            url = reverse('accounts:success')

            return HttpResponseRedirect(url)

        else:
            context['message'] = f"{email} already exists."
        
    context['page_title'] = 'User Registration'

    return render(request, 'accounts/register.html', context)

def success(request):
    context = {}
    return render(request, 'accounts/success.html', context)

def activate(request, hex_code):
    context = {}
    NOT_VALID = 'Hex code is not valid.'

    if settings.HEX_CODE_LENGTH != len(hex_code):
        context['message'] = NOT_VALID

    hex_code_object = HexString.objects.filter(code=hex_code).first()

    if hex_code_object and not helper.is_expired(hex_code_object.generated_at):
        manushya = Manushya.objects.filter(id=hex_code_object.manushya.id).first()
        manushya.is_active = 1
        manushya.save()
        hex_code_object.delete()
    else:
        context['message'] = NOT_VALID

    if 'message' in context:
        return render(request, 'accounts/failure.html', context)

    url = reverse('accounts:siyaram')
    return HttpResponseRedirect(url)

def siyaram(request):
    context = {}
    context['user'] = request.user
    return render(request, 'accounts/siyaram.html', context)

@csrf_protect
@require_http_methods(["GET", "POST"])
def account_login(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'accounts/login.html', context)

    postdata = request.POST.copy()
    email = postdata.get('email','')
    password = postdata.get('inputPassword1','')
    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        url = reverse('accounts:siyaram')
        return HttpResponseRedirect(url)

    context['message'] = 'Credential not valid.'
    return render(request, 'accounts/login.html', context)

@login_required
def account_logout(request):
    logout(request)

    context = {}
    if request.method == 'GET':
        return render(request, 'accounts/login.html', context)

@login_required
def profile(request):
    context = {}
    return render(request, 'accounts/profile.html', context)

@login_required
def search(request):
    context = {}
    return render(request, 'accounts/search.html', context)


