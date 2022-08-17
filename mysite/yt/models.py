from django.db import models
from django.db.models import CharField,TextField
from django_mysql.models import ListCharField,ListTextField
from django.contrib.auth.models import User
#from django_quill.fields import QuillField


class Tag(models.Model):

    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name


class KingTag(Tag):

    parentTag = models.ForeignKey(Tag, related_name='childTag', default=1, on_delete=models.SET_DEFAULT)
    address_name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.tag_name


class Video(models.Model):

    thumbnail = CharField(max_length=300, default='')
    title = CharField(max_length=300, default='')
    tag = models.ManyToManyField(Tag, related_name='videos')
    video_id = models.CharField(max_length=200, primary_key=True, default='')

    def __str__(self):
        return self.title


class Channel(models.Model):

    tag = models.ManyToManyField(Tag, related_name='tagged')
    chan_id = models.CharField(max_length=200)
    chan_keyword = ListCharField(
        base_field=CharField(max_length=200),
        size=30,
        max_length=(30 * 201),
        default=[]
    )
    chan_img = models.CharField(max_length=200, default="")
    chan_title = models.CharField(max_length=200, default="")
    chan_description = models.TextField(default="")
    subscription_count = models.IntegerField(default=-1)
    chan_viewCount = models.BigIntegerField(default=-1)
    chan_videoThumb = ListCharField(
        base_field=CharField(max_length=300),
        size=5,
        max_length=(5 * 301),
        default=[]
    )
    chan_videoTitle = ListTextField(
            base_field=CharField(max_length=300),
            size=5,
            default=[]
    )
    video = models.ManyToManyField(Video, related_name='channel')


    def __str__(self):
        return self.chan_title


class Update(models.Model):

    tag = models.ForeignKey(Tag, related_name='a', on_delete=models.CASCADE)
    kingtag = models.ForeignKey(KingTag, related_name='b', on_delete=models.CASCADE)
    address_name = models.CharField(max_length=200)


    def __str__(self):

        return self.tag.__str__()


class ToFix(models.Model):

    chan_id = models.CharField(max_length=200)
    errorType = models.CharField(max_length=200)

    def __str__(self):
        return self.chan_id
#-----------------------------------------#

class BoardMember(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth = models.IntegerField(default=0, null=0)

    def __str__(self):
        return self.username


class Category(models.Model):
    e_name = models.CharField(max_length=200, null=True, verbose_name="영어카테고리")
    name = models.CharField(max_length=200, null=True, verbose_name="카테고리")

    def __str__(self):
        return self.name


class Board(models.Model):
        
    title = models.CharField(max_length=200, verbose_name="작성자")
    contents = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(BoardMember, on_delete=models.CASCADE, verbose_name="작성자")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="카테고리", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="최종수정일")

    def __str__(self):
        return self.title


class Comment(models.Model):

    author = models.ForeignKey(BoardMember, on_delete=models.CASCADE, verbose_name="작성자", null=True)
    comment = models.TextField(verbose_name="")
    date = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    post = models.ForeignKey(Board, null=True, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(auto_now_add=True, verbose_name="수정일", null=True)
                                                                    
    def __str__(self):
        return self.comment

