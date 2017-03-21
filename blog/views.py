from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Max
from .models import Post, Comment, Nickname
from .forms import PostForm, CommentForm

def board(request):
    posts = Post.objects.order_by('id')
    return render(request, 'blog/board.html', {'posts':posts})

def thread(request, pk):
    post = get_object_or_404(Post, pk=pk) 
    posts = Post.objects.filter(thread_no=post.thread_no).order_by('created_date')
    return render(request, 'blog/thread.html', {'posts':posts, 'user':request.user})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html',{'post':post, 'form':CommentForm()})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.thread_no = Post.objects.aggregate(Max('thread_no'))['thread_no__max']+1
            post.nickname = Nickname.objects.get(aid=post.author.id,tno=post.thread_no).name
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.nickname = Nickname.objects.get(aid=post.author.id,tno=post.thread_no).name
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

def post_reply(request, pk):
    parent_post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.thread_no = parent_post.thread_no
            post.nickname = Nickname.objects.get(aid=post.author.id,tno=post.thread_no).name
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_reply.html', {'form': form})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.nickname = Nickname.objects.get(aid=comment.author.id,tno=post.thread_no).name
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        print 'method is not POST'

def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
