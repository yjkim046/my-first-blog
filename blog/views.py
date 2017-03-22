from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Max
from .models import Post, Comment, Nickname
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

@login_required
def board(request):
    posts = Post.objects.order_by('id')
    return render(request, 'blog/board.html', {'posts':posts})

@login_required
def thread(request, pk):
    post = get_object_or_404(Post, pk=pk) 
    posts = Post.objects.filter(thread_no=post.thread_no).order_by('created_date')
    r = Nickname.objects.aggregate(Max('aid'))['aid__max']
    c = Nickname.objects.aggregate(Max('tno'))['tno__max'] 
    nickname = Nickname.objects.get(aid=(request.user.id-1)%r+1,tno=(post.thread_no-1)%c+1).name
    return render(request, 'blog/thread.html', {'posts':posts, 'nickname':nickname, 'form':CommentForm()})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    r = Nickname.objects.aggregate(Max('aid'))['aid__max']
    c = Nickname.objects.aggregate(Max('tno'))['tno__max']
    nickname = Nickname.objects.get(aid=(request.user.id-1)%r+1,tno=(post.thread_no-1)%c+1).name
    return render(request, 'blog/post_detail.html',{'post':post, 'nickname':nickname, 'user':request.user, 'form':CommentForm()})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            posts = Post.objects.all()
            if not posts:
                post.thread_no = 1
            else:
                post.thread_no = Post.objects.aggregate(Max('thread_no'))['thread_no__max']+1
            r = Nickname.objects.aggregate(Max('aid'))['aid__max']
            c = Nickname.objects.aggregate(Max('tno'))['tno__max'] 
            post.nickname = Nickname.objects.get(aid=(post.author.id-1)%r+1,tno=(post.thread_no-1)%c+1).name
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            r = Nickname.objects.aggregate(Max('aid'))['aid__max']
            c = Nickname.objects.aggregate(Max('tno'))['tno__max'] 
            post.nickname = Nickname.objects.get(aid=(post.author.id-1)%r+1,tno=(post.thread_no-1)%c+1).name
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_reply(request, pk):
    parent_post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.thread_no = parent_post.thread_no
            r = Nickname.objects.aggregate(Max('aid'))['aid__max']
            c = Nickname.objects.aggregate(Max('tno'))['tno__max'] 
            post.nickname = Nickname.objects.get(aid=(post.author.id-1)%r+1,tno=(post.thread_no-1)%c+1).name
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_reply.html', {'form': form})

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            r = Nickname.objects.aggregate(Max('aid'))['aid__max']
            c = Nickname.objects.aggregate(Max('tno'))['tno__max'] 
            comment.nickname = Nickname.objects.get(aid=(comment.author.id-1)%r+1,tno=(post.thread_no-1)%c+1).name
            comment.save()
            return redirect('post_detail', pk=post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
