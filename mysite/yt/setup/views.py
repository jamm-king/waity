import django
django.setup()
from django.shortcuts import render
from youtube_api import YouTubeDataAPI
from ..models import *
from ..methods import get_charfield
from multiprocessing import Pool
from tqdm import tqdm
import time


def setup_Tag():
    
    nothing = KingTag.objects.create(tag_name='NOTHING', address_name="nothing", id=1, parentTag_id=1)

    game = KingTag.objects.create(tag_name='게임', address_name="game", id=2, parentTag=nothing)
    music = KingTag.objects.create(tag_name='음악', address_name= "music", id=3, parentTag=nothing)
    eat = KingTag.objects.create(tag_name='먹방', address_name="eat", id=4, parentTag=nothing)
    sports = KingTag.objects.create(tag_name='스포츠', address_name="sports", id=5, parentTag=nothing)
    entertain = KingTag.objects.create(tag_name='연예', address_name="entertain", id=6, parentTag=nothing)
    knowledge = KingTag.objects.create(tag_name='잡지식', address_name="knowledge", id=7, parentTag=nothing)
    review = KingTag.objects.create(tag_name='영화리뷰', address_name="review", id=8, parentTag=nothing)
    documentary = KingTag.objects.create(tag_name='다큐멘터리', address_name="documentary", id=9, parentTag=nothing)
    vlog = KingTag.objects.create(tag_name='브이로그', address_name="vlog", id=10, parentTag=nothing)
    # etc = Tag(tag_name='기타')

    # 게임
    leagueoflegend = KingTag.objects.create(tag_name="리그오브레전드", address_name="leagueoflegend", id=21, parentTag=game)
    battleground = KingTag.objects.create(tag_name='배틀그라운드', address_name="battleground", id=22, parentTag=game)
    overwatch = KingTag.objects.create(tag_name='오버워치', address_name="overwatch", id=23, parentTag=game)
    starcraft = KingTag.objects.create(tag_name='스타크래프트', address_name="starcraft", id=24, parentTag=game)
    maplestory = KingTag.objects.create(tag_name='메이플스토리', address_name="maplestory", id=25, parentTag=game)
    minecraft = KingTag.objects.create(tag_name='마인크래프트', address_name="minecraft", id=26, parentTag=game)
    fifa = KingTag.objects.create(tag_name='피파', address_name="fifa", id=27, parentTag=game)

    # game_etc = Tag(tag_name='기타 게임')

    # 음악
    sing = KingTag.objects.create(tag_name='노래', address_name="sing", id=31, parentTag=music)
    piano = KingTag.objects.create(tag_name='피아노', address_name="piano", id=32, parentTag=music)
    mv = KingTag.objects.create(tag_name='뮤비', address_name="mv", id=33, parentTag=music)
    classic = KingTag.objects.create(tag_name='클래식', address_name="classic", id=34, parentTag=music)
    audition = KingTag.objects.create(tag_name='오디션', address_name="audition", id=35, parentTag=music)
    hiphop = KingTag.objects.create(tag_name='힙합', address_name="hiphop", id=36, parentTag=music)
    trott = KingTag.objects.create(tag_name='트로트', address_name="trott", id=37, parentTag=music)
    popsong = KingTag.objects.create(tag_name='팝송', address_name="popsong", id=38, parentTag=music)
    kpop = KingTag.objects.create(tag_name='K팝', address_name="kpop", id=39, parentTag=music)
    # music_etc = Tag(tag_name='기타 음악')

    # 스포츠
    soccer = KingTag.objects.create(tag_name='축구', address_name="soccer", id=51, parentTag=sports)
    basketball = KingTag.objects.create(tag_name='농구', address_name="basketball", id=52, parentTag=sports)
    baseball = KingTag.objects.create(tag_name='야구', address_name="baseball", id=53, parentTag=sports)
    golf = KingTag.objects.create(tag_name='골프', address_name="golf", id=54, parentTag=sports)
    tennis = KingTag.objects.create(tag_name='테니스', address_name="tennis", id=55, parentTag=sports)
    # sports_etc = Tag(tag_name='기타 스포츠', id=51, parentTag=sports)

    # 연예
    idol = KingTag.objects.create(tag_name='아이돌', address_name="idol", id=61, parentTag=entertain)
    play = KingTag.objects.create(tag_name='예능', address_name="play", id=62, parentTag=entertain)
    # entertain_etc = Tag(tag_name='기타 연예')

    return "Tag Set Done"


def setup_Channel():
    api_key = 'AIzaSyBzXpb-djwWT18JGwQCWLS3Fg4B_ZVLFfQ'
    yt = YouTubeDataAPI(api_key)
    origin_tagQuerySet = KingTag.objects.all()[1:]
    cnt = 0
    for origin_tag in origin_tagQuerySet:
        searches = yt.search(origin_tag.tag_name, max_results=10)
        for new_channel in searches:
            id = new_channel['channel_id']
            doesExist = 0
            origin_channelQuerySet = Channel.objects.all()
            if origin_channelQuerySet.__len__() != 0:
                for origin_channel in origin_channelQuerySet:
                    if id == origin_channel.chan_id:
                        origin_channel.tag.add(origin_tag)
                        if origin_tag.parentTag.tag_name != "NOTHING":
                            origin_channel.tag.add(origin_tag.parentTag)
                        origin_channel.save()
                        doesExist = 1
                if doesExist == 0:
                    c = Channel.objects.create(chan_id=id)
                    c.tag.add(origin_tag)
                    if origin_tag.parentTag.tag_name != "NOTHING":
                        c.tag.add(origin_tag.parentTag)
                    target_url = 'https://m.youtube.com/channel/{}'.format(id)
                    try:
                        info = get_charfield(target_url)
                        c.chan_title = info['title']
                        c.chan_keyword = info['keywords']
                        c.subscription_count = info['subscription_count']
                        c.chan_videoThumb = info['videoThumb'][:5]
                       # c.chan_description = info['description']
                        c.chan_viewCount = info['viewCount']
                        c.chan_img = info['img']
                        c.chan_videoTitle = info['videoTitle'][:5]
                        c.save()
                        print(c.chan_title + ' channel set')
                    except:
                        print(c.chan_title + ' something wrong happend')
            else:
                c = Channel.objects.create(chan_id=id)
                c.tag.add(origin_tag)
                if origin_tag.parentTag.tag_name != "NOTHING":
                    c.tag.add(origin_tag.parentTag)
                target_url = "https://youtube.com/channel/{}".format(id)
                try:
                    info = get_charfield(target_url)
                    c.chan_title = info['title']
                    c.chan_keyword = info['keywords']
                    c.subscription_count = info['subscription_count']
                    c.chan_videoThumb = info['VideoThumb'][:5]
                   # c.chan_description = info['description']
                    c.chan_viewCount = info['viewCount']
                    c.chan_img = info['img']
                    c.save()
                    print(c.chan_title + 'channel set')
                except:
                    print(c.chan_title + 'something wrong happend')


    return "Channel Set Done"


def make_keywordTag():
    channelSet = Channel.objects.all()
    k = []
    for channel in tqdm(channelSet):
        for name in channel.chan_keyword:
            tagSet = Tag.objects.all()
            doesExist = False
            for tag in tagSet:
                if tag.tag_name == name:
                    doesExist = True
                    channel.tag.add(tag)
                    break
            if doesExist == False:
                newTag = Tag()
                newTag.tag_name = name
                newTag.save()
                channel.tag.add(newTag)
                channel.save()
            else:
                pass
         


    return "keywordTags are successfully made"


def get_id():
    channelSet = Channel.objects.all()
    context = []
    for channel in channelSet:
        context.append(channel.chan_id)
    return context


def update_Channel(id):
    # val : 'title' ,'keywords', 'subscription_count' , 'videoThumb' , 'description' , 'viewCount'
    channel = Channel.objects.filter(chan_id=id).get()
    target_url = 'https://www.youtube.com/channel/{}'.format(channel.chan_id)
    try:
        info = get_charfield(target_url)
        channel.chan_title = info['title']
        channel.chan_keyword = info['keywords']
        channel.subscription_count = info['subscription_count']
        channel.chan_videoThumb = info['videoThumb'][:5]
        channel.chan_viewCount = info['viewCount']
        channel.chan_img = info['img']
        channel.chan_videoTitle = info['videoTitle'][:5]

        if len(channel.chan_videoThumb) < 5:
            print(channel.chan_title + " too few videos")
            ToFix.objects.create(chan_id=channel.chan_id, errorType="too few videos")
        else:
            channel.save()
            print(channel.chan_title + ' updated')

    except Exception as e:
        print(channel.chan_title + ' failed!!!!!')
        print(e)
        ToFix.objects.create(chan_id=channel.chan_id, errorType=str(e))

    for tag in channel.tag.all():
        try:
            if tag.kingtag.parentTag.tag_name != 'NOTHING':
                channel.tag.add(tag.kingtag.parentTag)
        except:
            pass

    if channel.chan_title == '없음':
        channel.delete()


def setup_Video():
    channels = Channel.objects.all()
    for channel in tqdm(channels):
        for i in range(5):
            try:
                _thumbnail = channel.chan_videoThumb[i]
                _title = channel.chan_videoTitle[i]
                _video_id = _thumbnail[23:34]
                _video = Video.objects.create(thumbnail=_thumbnail, title=_title, video_id=_video_id)
                channel.video.add(_video)
            except:
                pass

    return "New Videos created"


def handle_ToFix():
    TF = ToFix.objects.all()
    for tf in TF:
        print('--------------------------------------------')
        print(tf.chan_id, tf.errorType)
        print('1: delete    2: pass')
        print('--------------------------------------------')
        a = input()
        if a == '1':
            tf.delete()
        else:
            pass

    return "done"


def UPDATE():
    ids = get_id()
    for id in ids:
        update_Channel(id)
    make_keywordTag()
    setup_Video()

    return "Update Done"

def CREATE_CSV():
    waityDB = pymysql.connect(
        user = 'deploy',
        passwd = '',
        host = 'localhost',
        db = 'yt',
        charset = 'utf8mb4'
    )
    cursor = waityDB.cursor(pymysql.cursors.DictCursor)
    tags = {'game': 2, 'music': 3, 'eat': 4, 'sports': 5, 'entertain': 6, 'knowledge': 7, 'review': 8,
            'documentary': 9, 'vlog': 10, 'leagueoflegend': 21, 'battleground': 22, 'overwatch': 23,
            'starcraft': 24, 'maplestory': 25, 'minecraft': 26, 'fifa': 27, 'sing': 31, 'piano': 32, 'mv': 33,
            'classic': 34, 'audition': 35, 'hiphop': 36, 'trott': 37, 'popsong': 38, 'kpop': 39, 'soccer': 51,
            'basketball': 52, 'baseball': 53, 'golf': 54, 'tennis': 55, 'idol': 61, 'play': 62}
    items = tags.items()
    data_dir = '/srv/waity/colab/csv/'

    for k, v in items:

        sql = 'select * from ( select distinct yt_video.video_id, yt_video.title, yt_video.thumbnail from yt_video, yt_video_tag where (yt_video.video_id = yt_video_tag.video_id) and (yt_video_tag.tag_id = ' + str(v) + ') )tb;'
        cursor.execute(sql)
        result = cursor.fetchall()
        data1 = result
        for d in data1:
            d['tag_id'] = 1

        sql = 'select * from ( select distinct yt_video.video_id, yt_video.title, yt_video.thumbnail from yt_video, yt_video_tag where (yt_video.video_id = yt_video_tag.video_id) and (yt_video_tag.tag_id != ' + str(v) + ') )tb;'
        cursor.execute(sql)
        result = cursor.fetchall()
        data2 = result
        for d in data2:
            d['tag_id'] = 0

        data = data1 + data2

        _fieldnames = ['video_id', 'title', 'thumbnail', 'tag_id']
        f = open(data_dir + k + '.csv', 'w', encoding='utf-8')
        writer = csv.DictWriter(f, fieldnames=_fieldnames)
        writer.writeheader()
        writer.writerows(data)
        f.close()

        sql = 'select count(*) from ( select distinct yt_video.video_id, yt_video.title, yt_video.thumbnail from yt_video, yt_video_tag where (yt_video.video_id = yt_video_tag.video_id) and (yt_video_tag.tag_id = ' + str(v) + ') )tb;'
        cursor.execute(sql)
        result = cursor.fetchall()
        cnt = result[0]['count(*)'] * 2
        print(result, type(result))
        df = pd.read_csv('datas\\' + k + '.csv')
        df2 = df.duplicated(['video_id'],keep='first')
        dup_idx=[]
        for idx,flag in enumerate(df2):
            if flag == True:
                dup_idx.append(idx)
        for i in reversed(dup_idx):
            df.drop(df.index[i],axis=0,inplace=True)
        df3 = df.loc[:cnt]
        df3.to_csv(data_dir + k + '_balanced.csv')