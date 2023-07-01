from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Post, Comment
from .form import  CommentForm
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def comment_create(request, post_id):
    """
    게시글에 대한 댓글 추가
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.created_at = timezone.now()
            comment.post = post
            comment.save()
            
            return redirect('community:community_detail', post_id = post.id)
    else:
        form = CommentForm()
        
    context = {'form' : form}
    return render(request, './community/comment_form.html', context)

def comment_modify(request, comment_id):
    """
    게시글에 대한 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user:
        messages.error(request, '수정 권한이 없습니다. . 😅')
        return redirect('community:community_detail', post_id = comment.post.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.modify_date = timezone.now()
            comment.save()
        
            url = resolve_url('community:community_detail', post_id = comment.post.id)
            return redirect(f'{url}#comment_{comment.id}')
    else:
        form = CommentForm(instance=comment)
    
    context = {'form' : form}
    return render(request, 'community/comment_form.html', context)

def comment_delete(request, comment_id):
    """
    게시글에 대한 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user:
        messages.error(request, '삭제 권한이 없습니다. . 😅')
        return redirect('community:community_detail', post_id = comment.post.id)
    else:
       comment.delete()

    url = resolve_url('community:community_detail', post_id = comment.post.id)
    return redirect(url)