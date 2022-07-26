from bs4 import BeautifulSoup
import requests
import re


def get_charfield(target_url):

    val = {}
    html = requests.get(target_url).text
    soup = BeautifulSoup(html, 'lxml')

    #키워드
    c1 = soup.find('meta', {'name': 'keywords'}).get('content')
    filter = '동영상, 공유, 카메라폰, 동영상폰, 무료, 올리기'
    if filter == c1:
        k = []
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

    #채널 이름
    title = soup.find('meta', {'itemprop': 'name'}).get('content')

    #구독자 수
    pattern = '(구독자 (\d+[.]\d+(천|만|억)|(\d+(천|만|억))|\d+)명)'
    result = re.findall(pattern, html)
    #if temp == '':
    if result == []:
        sub_num = -1
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

    #썸네일
    pattern = 'https://i.ytimg.com/vi/[\d\w]+/hqdefault.jpg'
    result = re.findall(pattern, html)
    thumb_list = []
    for item in result:
        if item not in thumb_list:
            thumb_list.append(item)

    #이미지
    img = soup.find('meta', {'property': 'og:image'}).get('content')

    #설명
   # desc = soup.find('meta', {'itemprop': 'description'}).get('content')

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

    val['keywords'] = k
    val['subscription_count'] = sub_num
    val['title'] = title
    val['videoThumb'] = thumb_list
    val['img'] = img
    #val['description'] = desc
    val['viewCount'] = cnt

    #val : 'title', 'keywords', 'subscription_count', 'videoThumb', 'description', 'viewCount','img'

    return val
