import django
django.setup()
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .methods import Autocomplete, ItemDesc, AddressNames, PageObject_Channel
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm

def loginpractice(request):
    return render(request,'yt/loginpractice.html')

def sooker(request):
    return render(request,'yt/sooker.html')

def practice(request):

    return render(request, 'yt/practice.html')

def index(request):

    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/index.html', context)


def setup(request):
    return render(request, 'yt/setup.html')


def search(request):

    str = request.GET.get('query')
    try:
        tag = Tag.objects.filter(tag_name=str).get()
    except ObjectDoesNotExist:
        messages.info(request, "없는 태그입니다.")
        return redirect('yt:index')

    if tag.tag_name == "NOTHING":
        messages.info(request, "없는 태그입니다.")
        

    page_obj = PageObject_Channel(request, str)

    tagArray = Autocomplete()

    context = {'channelSet': page_obj, 'tagArray': tagArray, 'query': str}

    return render(request, 'yt/search.html', context)


def home(request):

    user_id = request.session.get('user')
    if user_id:
        member = BoardMember.objects.get(pk=user_id)
        return HttpResponse(member.username)

    return HttpResponse('home!')


def login(request):
    if 'user' in request.session:
        return redirect('yt:index')

    if request.method == 'POST':
        print(request.POST)
        #f5가 눌러졌으면? 새로운 폼을 보여줘야함..
        form = LoginForm(request.POST)

        if form.is_valid():
            request.session['user'] = form.user_id
            request.session['auth'] = form.user_auth
            if 'pre_page' in request.session:
                pre_page = request.session['pre_page']
                del(request.session['pre_page'])
                return redirect(pre_page)
            else:
                return redirect('yt:index')

    else:
        if request.GET.get('path'):
            print(request.GET.get('path'))
        form = LoginForm()

    return render(request, 'yt/login.html', {'form': form})


def logout(request):

    if request.session.get('user'):
        del(request.session['user'])
        request.session.flush()

    return redirect('yt:index')


def register(request):
    if request.method == 'GET':
        return render(request, 'yt/register.html')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

        res_data = {}

        if password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            member = BoardMember(username=username,email=email,password=make_password(password))
            member.save()

        if res_data == {}:
            print('to index')
            return redirect('yt:index')
        else:
            print('to register')
            return render(request, 'yt/register.html', res_data)

