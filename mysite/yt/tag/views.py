from django.shortcuts import render
from ..methods import PageObject_All, PageObject_Tag, PageObject_Channel, Autocomplete, ItemDesc, AddressNames
from ..models import *


def all(request):

    if request.method == 'GET':
        page_obj = PageObject_All(request)
        tagArray = Autocomplete()
        context = ItemDesc()
        kingTags = KingTag.objects.all()[1:]
        context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}
        return render(request, 'yt/tag/videos.html', context) 

    elif request.method == 'POST':
        page_obj = PageObject_All(request)
        for i in range(len(page_obj)):
            tag = request.POST.getlist('tag'+str(i))
            video = page_obj[i]
            # 기존태그 삭제     
            v = video.tag.all()
            for j in v:
                video.tag.remove(j)
            # 새롭게 정의한 태그    
            for t in tag:
                video.tag.add(Tag.objects.filter(tag_name=t).get())
            video.save()
        for i in range(len(page_obj)):
            video = page_obj[i]
            print(video.tag.all())

        tagArray = Autocomplete()
        context = ItemDesc()
        kingTags = KingTag.objects.all()[1:]
        context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}
        return render(request, 'yt/tag/videos.html', context) 


def game(request):

    page_obj = PageObject_Tag(request, '게임')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/tags.html', context)


def leagueoflegend(request):

    page_obj = PageObject_Channel(request, '리그오브레전드')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}
    return render(request, 'yt/tag/channels.html', context)


def battleground(request):

    page_obj = PageObject_Channel(request, '배틀그라운드')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def overwatch(request):

    page_obj = PageObject_Channel(request, '오버워치')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def starcraft(request):

    page_obj = PageObject_Channel(request, '스타크래프트')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def maplestory(request):

    page_obj = PageObject_Channel(request, '메이플스토리')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def minecraft(request):

    page_obj = PageObject_Channel(request, '마인크래프트')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def fifa(request):

    page_obj = PageObject_Channel(request, '피파')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def music(request):

    page_obj = PageObject_Tag(request, '음악')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/tags.html', context)


def sing(request):

    page_obj = PageObject_Channel(request, '노래')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def piano(request):

    page_obj = PageObject_Channel(request, '피아노')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def mv(request):

    page_obj = PageObject_Channel(request, '뮤비')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def classic(request):

    page_obj = PageObject_Channel(request, '클래식')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def audition(request):

    page_obj = PageObject_Channel(request, '오디션')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def hiphop(request):

    page_obj = PageObject_Channel(request, '힙합')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def trott(request):

    page_obj = PageObject_Channel(request, '트로트')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def popsong(request):

    page_obj = PageObject_Channel(request, '팝송')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def kpop(request):

    page_obj = PageObject_Channel(request, 'K팝')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def eat(request):

    page_obj = PageObject_Channel(request, '먹방')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def sports(request):

    page_obj = PageObject_Tag(request, '스포츠')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/tags.html', context)


def soccer(request):

    page_obj = PageObject_Channel(request, '축구')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def basketball(request):

    page_obj = PageObject_Channel(request, '농구')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def baseball(request):

    page_obj = PageObject_Channel(request, '야구')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def golf(request):

    page_obj = PageObject_Channel(request, '골프')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def tennis(request):

    page_obj = PageObject_Channel(request, '테니스')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def entertain(request):

    page_obj = PageObject_Tag(request, '연예')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/tags.html', context)


def idol(request):

    page_obj = PageObject_Channel(request, '아이돌')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)

def play(request):

    page_obj = PageObject_Channel(request, '예능')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def knowledge(request):

    page_obj = PageObject_Channel(request, '잡지식')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def review(request):

    page_obj = PageObject_Channel(request, '영화리뷰')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def documentary(request):

    page_obj = PageObject_Channel(request, '다큐멘터리')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)


def vlog(request):

    page_obj = PageObject_Channel(request, '브이로그')
    tagArray = Autocomplete()
    context = ItemDesc()
    kingTags = AddressNames()
    context = {'page_obj': page_obj, 'tagArray': tagArray, 'kingTags': kingTags, 'context': context}

    return render(request, 'yt/tag/channels.html', context)
