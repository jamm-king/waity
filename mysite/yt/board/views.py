import django
import datetime
from django.contrib import messages
django.setup()
from django.shortcuts import render, redirect
from ..methods import PageObject_Board
from ..models import *
from .forms import *
from django.http import Http404
from django.core.paginator import Paginator

def myBoardDelete(request):
    lis = []
    if request.method == 'POST':
        data = request.POST['delete_data']
        lis = data.split(',')
        for val in lis:
            board = Board.objects.filter(id=val)
            board.delete()
        return redirect('yt:myBoard')

def myBoard(request):

    if 'user' in request.session:
        boards = Board.objects.filter(writer_id=request.session['user'])

        return render(request, 'yt/board/myBoard.html', {'page_obj': boards})
    else:
        request.session['pre_page'] = request.build_absolute_uri()
        return redirect('yt:login')


def BoardModify(request, board_id):

    board = Board.objects.filter(id=board_id).get()
    if request.method == 'POST':
        board.title = request.POST['title']
        board.contents = request.POST['contents']
        board.updated_at = datetime.datetime.now()
        board.save()
        return redirect('yt:boardDetail', board_id)
    else:
        form = BoardForm()

    return render(request, 'yt/board/modify.html', {'board': board, 'form': form})


def CommentModify(request, comment_id):

    comment = Comment.objects.filter(id=comment_id).get()
    post_id = comment.post_id

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Board.objects.filter(id=post_id).get()
            comment.author_id = request.session['user']
            comment.modify_date = datetime.datetime.now()
            comment.save()
            return redirect('yt:boardDetail', post_id)
    else:
        form = CommentForm()

    return redirect('yt:boardDetail', post_id)


def CommentDelete(request, comment_id):

    comment = Comment.objects.filter(id=comment_id).get()
    post_id = comment.post_id

    comment.delete()

    return redirect('yt:boardDetail', post_id)


def new_comment(request, post_id):

    if not request.session.get('user'):
        request.session['pre_page'] = request.build_absolute_uri()
        return redirect('yt:login')

    form = CommentForm(request.POST)
    if form.is_valid():
        finished_form = form.save(commit=False)
        finished_form.post = Board.objects.filter(pk=post_id).get()
        finished_form.author_id = request.session['user']
        finished_form.save()

    return redirect('yt:boardDetail', post_id)

def Board_list(request):

    category = Category.objects.filter(e_name='all').get()
    categories = Category.objects.all()
    page_obj = PageObject_Board(request)
    return render(request, 'yt/board/list.html', {'page_obj': page_obj, 'filter': category, 'categories': categories})


def Board_detail(request, pk):

    comment_form = CommentForm()
    try:
        board = Board.objects.get(pk=pk)
        try:
            user = request.session['user']
        except:
            user = 0
    except:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'yt/board/detail.html', {'board': board, 'comment_form': comment_form, 'user': user})


def Board_write(request):

    if not request.session.get('user'):
        request.session['pre_page'] = request.build_absolute_uri()
        return redirect('yt:login')
    if request.method == "POST":
        if request.session['auth'] == 1:
            form = BoardForm_admin(request.POST)
        else:
            form = BoardForm(request.POST)

        if form.is_valid():
            # form의 모든 validators 호출 유효성 검증 수행
            user_id = request.session.get('user')
            member = BoardMember.objects.get(pk=user_id)

            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            category_name = form.cleaned_data['category']
            category = Category.objects.filter(e_name=category_name).get()
            board.category = category
            # 검증에 성공한 값들은 사전타입으로 제공 (form.cleaned_data)
            # 검증에 실패시 form.error 에 오류 정보를 저장

            board.writer = member
            board.save()
            print(1)
            return redirect('yt:boardList')

    else:
        if request.session['auth'] == 1:
            form = BoardForm_admin()
        else:
            form = BoardForm()
    print(2)
    return render(request, 'yt/board/write.html', {'form': form})


def Board_category(request, category_name):

    categories = Category.objects.all()
    if category_name == 'all':
        page_obj = PageObject_Board(request)
        category = Category.objects.filter(e_name='all').get()
    else:
        category = Category.objects.filter(e_name=category_name).get()
        boards = Board.objects.filter(category=category).all().order_by('-id')
        page = request.GET.get('page', '1')
        paginator = Paginator(boards, 20)
        page_obj = paginator.get_page(page)

    return render(request, 'yt/board/list.html', {'page_obj': page_obj, 'filter': category, 'categories': categories})
