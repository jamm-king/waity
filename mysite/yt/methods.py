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
    video = Video.objects.all()
    obj = []
    for v in video:
        t = v.tag.all()
        o = {'video': v, 'tag': t}
        obj.append(o)
    page = request.GET.get('page', '1')
    paginator = Paginator(obj, 8)
    page_obj = paginator.get_page(page)
    return page_obj


def PageObject_All2(request):
    video = Video.objects.all()
    obj = []
    for v in video:
        t = v.tag.all()
        o = {'video': v, 'tag': t}
        obj.append(o)
    page = request.POST.get('page', '1')
    paginator = Paginator(obj, 8)
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
    val['title'] = title

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

    #영상 크롤링 Regular expression 
    # pattern = '{"url":"[^"]+","width"[^"]+"height"[^"]+"title":{"accessibility":{"accessibilityData":{"label":"[^"]+"}}'
    # p1 = '"url":"[^"]+","width"[^"]+"height"[^"]+"'
    # p2 = '"title":{"accessibility":{"accessibilityData":{"label":"[^"]+"'
    # p3 = 'https://i.ytimg.com/vi/[^/]+/hqdefault'
    # p4 = '"title":{"accessibility":{"accessibilityData":{"label":"'
    # p5 = '\\s게시자:[^"]+"'

    # result = re.findall(pattern, html)[:5]
    # thumb_list = []
    # title_list = []
    # for item in result:
    #     thumbnail = re.findall(p3, re.findall(p1, item)[0])[0] + '.jpg'
    #     title = re.sub(p5, '', re.sub(p4, '', re.findall(p2, item)[0]))
    #     title = title.replace(',', '')
    #     thumb_list.append(thumbnail)
    #     title_list.append(title)

    # val['videoThumb'] = thumb_list
    # val['videoTitle'] = title_list
    data = soup.find_all('script')[33]
    data = str(data.contents[0])
    data = data.replace('var ytInitialData = ','')
    data = data.replace(';','')
    json_data = json.loads(data)

    thumb_list = []
    title_list = []
    videos = ""
    try:
        # 채널 가장 위에 영상 or 실시간 없는경우 
        videos = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['horizontalListRenderer']['items']


    except:
        # 채널 가장 위에 영상 or 실시간 있는경우 -> [1]
        videos = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][1]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['horizontalListRenderer']['items']


    for i,video in enumerate(videos):
        if i == 5:
            break
        title_list.append(video['gridVideoRenderer']['title']['simpleText'])
        thumbnail = video['gridVideoRenderer']['thumbnail']['thumbnails'][0]['url']
        thumbnail = thumbnail.split('hqdefault')[0] + 'hqdefault.jpg'
        thumb_list.append(thumbnail)

    val['videoThumb'] = thumb_list
    val['videoTitle'] = title_list

    #이미지
    img = soup.find('meta', {'property': 'og:image'}).get('content')
    val['img'] = img

    #설명
    desc = soup.find('meta', {'itemprop': 'description'}).get('content')
    val['description'] = desc

    #조회수
    html = requests.get(target_url + '/about').text
    soup = BeautifulSoup(html, 'lxml')
    pattern = '조회수 [,\d]+회'
    temp2 = re.search(pattern, html)
    if temp2 == None:
        cnt = -1
    else:
        temp2 = temp2.group()
        cnt = re.sub('조회수| |회|,', '', temp2)
        cnt = int(cnt)
    val['viewCount'] = cnt

    #val : 'title', 'keywords', 'subscription_count', 'videoThumb', 'description', 'viewCount','img', 'videoTitle'
    return val
