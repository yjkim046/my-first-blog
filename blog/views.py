from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Max
from .models import Post, Comment, Nickname
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

def get_nickname(user_id, thread_no):
    max_nid = Nickname.objects.aggregate(Max('nid'))['nid__max']
    if user_id==1:
        nickname = Nickname.objects.get(nid=0).name
    else:
        nickname = Nickname.objects.get(nid=(user_id+3*thread_no)%max_nid+1).name
    if user_id>max_nid:
        nickname = nickname + str(user_id/max_nid+1)
    return nickname

@login_required
def about(request):
    return render(request, 'blog/about.html')

@login_required
def board(request):
    posts = Post.objects.order_by('id')
    return render(request, 'blog/board.html', {'posts':posts, 'user':request.user})

@login_required
def thread(request, pk):
    post = get_object_or_404(Post, pk=pk) 
    posts = Post.objects.filter(thread_no=post.thread_no).order_by('created_date')
    nickname = get_nickname(request.user.id,post.thread_no)
    return render(request, 'blog/thread.html', {'posts':posts, 'nickname':nickname})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    nickname = get_nickname(request.user.id,post.thread_no)
    post.num_read+=1
    post.save()
    return render(request, 'blog/post_detail.html', {'post':post, 'nickname':nickname, 'user':request.user, 'form':CommentForm()})

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
                post.thread_no = 0
            else:
                post.thread_no = Post.objects.aggregate(Max('thread_no'))['thread_no__max']+1
            post.nickname = get_nickname(request.user.id,post.thread_no)
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
            post.nickname = get_nickname(request.user.id,post.thread_no)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        parent_text = '> '+parent_post.nickname+' wrote:\n-----------------------\n'+parent_post.text
        initial_text = '\n\n'+'\n> '.join(parent_text.splitlines()) 
        form = PostForm(initial={'title':'RE: '+parent_post.title, 'text':initial_text})
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')

@login_required
def post_recommend(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.num_recommendation+=1 
    post.save() 
    return redirect('post_detail', pk=post.pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.nickname = get_nickname(request.user.id,post.thread_no)
            if "Save" in request.POST:
                post.num_user_comment+=1
                post.comment_cnt+=1
                comment.within_post_id = post.comment_cnt
            elif "Report" in request.POST:
                post.num_user_report+=1
                comment.within_post_id = 0
            comment.save()
            post.save()
            return redirect('post_detail', pk=post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if comment.within_post_id==0:
        post.num_user_report-=1
    else:
        post.num_user_comment-=1
    if comment.within_post_id==post.comment_cnt:
        post.comment_cnt-=1 
    post.save()
    comment.delete()
    return redirect('post_detail', pk=post.pk)
