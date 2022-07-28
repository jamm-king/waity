from bs4 import BeautifulSoup
import re, requests, json
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q


#parsing for javascript
def Autocomplete():
    tagSet = Tag.objects.all()
    parsed = []
    for tag in tagSet:
        if tag.tag_name != "NOTHING":
            parsed.append(tag.tag_name)
    tagArray = json.dumps(parsed)
    return tagArray


def AddressNames():
    tagSet = KingTag.objects.all()
    parsed = []
    for tag in tagSet:
        if tag.tag_name != "NOTHING":
            parsed.append(tag.address_name)
    addressNames = json.dumps(parsed)
    return addressNames


def ItemDesc():
    tagSet = KingTag.objects.all()
    tagList = []
    for tag in tagSet:
        if tag.tag_name != "NOTHING":
            tagList.append(tag.address_name)
    parsed = {}
    for tag in tagList:
        channelSet = KingTag.objects.filter(address_name=tag).get().tagged.all().order_by('-subscription_count')
        count = channelSet.count()
        images = []
        for c in channelSet:
            images.append(c.chan_img)
        temp = {
            'count': count,
            'images': images[:9]
        }
        parsed[tag] = temp
    itemDesc = json.dumps(parsed)
    return itemDesc


def PageObject_Tag(request, tagName):
    tag = Tag.objects.filter(tag_name=tagName).get()
    kt = KingTag.objects.filter(parentTag=tag)
    page = request.GET.get('page', '1')
    paginator = Paginator(kt, 8)
    page_obj = paginator.get_page(page)
    return page_obj


def PageObject_Channel(request, tagName):
    tag = Tag.objects.filter(tag_name=tagName).get().tagged.all().order_by('-subscription_count', '-chan_viewCount')
    page = request.GET.get('page', '1')
    paginator = Paginator(tag, 8)
    page_obj = paginator.get_page(page)
    print(tag[0].chan_title)
    return page_obj

def PageObject_All(request):
    tag = Video.objects.all()
    page = request.GET.get('page', '1')
    paginator = Paginator(tag, 8)
    page_obj = paginator.get_page(page)
    return page_obj


def PageObject_Board(request):
    notice = Category.objects.filter(e_name='notice').get()
    boards_notice = Board.objects.filter(category=notice).order_by('-id')
    boards_etc = Board.objects.filter(~Q(category=notice)).order_by('-id')
    boards_notice = list(boards_notice)
    boards_etc = list(boards_etc)
    boards = boards_notice + boards_etc
    page = request.GET.get('page', '1')
    paginator = Paginator(boards, 20)
    page_obj = paginator.get_page(page)
    return page_obj


#크롤링
def get_charfield(target_url):

    val = {}
    html = requests.get(target_url).text
    soup = BeautifulSoup(html, 'lxml')

    #키워드
    c1 = soup.find('meta', {'name': 'keywords'}).get('content')
    filter = '동영상, 공유, 카메라폰, 동영상폰, 무료, 올리기'
    if filter == c1:
        val['keywords'] = []
    else:
        k = []
        word = ''
        swch = False
        swch2 = False
        for i in c1:
            if i == '"':
                if swch == True:
                        k.append(word)
                        word = ''
                        swch = False
                        swch2 = True
                else:
                    swch = True
            else:
                if i == ' ':
                    if swch == True:
                        word = word + i
                    else:
                        if swch2 == True:
                            swch2 = False
                        else:
                            k.append(word)
                            word = ''
                else:
                    word = word + i
        if word != '':
            k.append(word)
        val['keywords'] = k

    #채널 이름
    title = soup.find('meta', {'itemprop': 'name'}).get('content')

    #구독자 수
    pattern = '(구독자 (\d+[.]\d+(천|만|억)|(\d+(천|만|억))|\d+)명)'
    result = re.findall(pattern, html)
    #if temp == '':
    if result == []:
        val['subscription_count'] = -1
    else :
        #문자열에서 숫자만 추출
        temp = result[len(result) - 1][0]
        sub = re.sub('구독자|명| ', '', temp)
        sub_num = re.sub('천|만|억', '', sub)
        if temp.find('천') != -1:
            sub_num = float(sub_num)
            sub_num *= 1000
            sub_num = int(sub_num)
        elif temp.find('만') != -1:
            sub_num = float(sub_num)
            sub_num *= 10000
            sub_num = int(sub_num)
        elif temp.find('억') != -1:
            sub_num = float(sub_num)
            sub_num *= 100000000
            sub_num = int(sub_num)
        val['subscription_count'] = sub_num

    #썸네일
    pattern = 'https://i.ytimg.com/vi/[^/]+/hqdefault.jpg'
    result = re.findall(pattern, html)
    thumb_list = []
    for item in result:
        if item not in thumb_list:
            thumb_list.append(item)
    thumb_list = thumb_list[:5]
    val['title'] = title
    val['videoThumb'] = thumb_list

    #썸네일 제목
    h = re.sub('\\\\"', '', html)
    title_list = []
    pattern = '"title":{"accessibility":{"accessibilityData":{"label":"[^"]+"}}'
    iter1 = '"title":{"accessibility":{"accessibilityData":{"label":"'
    iter2 = '\s게시자:[^"]+"}}'
    result = re.findall(pattern, h)
    for item in result:
        item = re.sub(iter1, "", item)
        item = re.sub(iter2, "", item)
        item = item.replace(',','')
        title_list.append(item)
    title_list = title_list[:5]
    val['videoTitle'] = title_list

    #이미지
    img = soup.find('meta', {'property': 'og:image'}).get('content')
    val['img'] = img

    #설명
    desc = soup.find('meta', {'itemprop': 'description'}).get('content')

    html = requests.get(target_url + '/about').text
    soup = BeautifulSoup(html, 'lxml')

    #조회수
    pattern = '조회수 [,\d]+회'
    temp2 = re.search(pattern, html)
    if temp2 == None:
        cnt = -1
    else:
        temp2 = temp2.group()
        cnt = re.sub('조회수| |회|,', '', temp2)
        cnt = int(cnt)

    val['description'] = desc
    val['viewCount'] = cnt

    #val : 'title', 'keywords', 'subscription_count', 'videoThumb', 'description', 'viewCount','img'

    return val
