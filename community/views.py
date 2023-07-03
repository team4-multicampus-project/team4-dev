from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .form import PostForm
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def community_list(request):
    '''
    Community 목록 출력
    '''
    post_list = Post.objects.order_by('-created_at')
    
    context = {
        'post_list' : post_list,
    }
    return render(request, 'community/community_list.html', context)

def community_detail(request, post_id):
    '''
    Community 상세
    '''
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post' : post
    }
    
    return render(request, 'community/community_detail.html', context)

def create_post(request):
    '''
    글 작성
    '''
    if request.method == 'POST':
        form = PostForm(request.POST)
        # 여기서 request.FILES 하고 save 아래에서 하니까 아래 코드 한 줄 필요 없음!
        if form.is_valid():
            problem = form.save(commit=False)
            problem.created_at = timezone.now()
            problem.user = request.user
            problem.save()
            return redirect('community:community_list')
    else:
        form = PostForm()
        
    context = {'form': form}
        
    return render(request, 'community/community_form.html', context)

def delete_post(request, post_id):
    '''
    글 삭제
    '''
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user:
        messages.error(request, '삭제 권한이 없습니다. . 😅')
        return redirect('community:community_detail', post_id = post.id)
    post.delete()
    return redirect('community:community_list')

def modify_post(request, post_id):
    '''
    글 수정
    '''
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user:
        messages.error(request, '수정 권한이 없습니다. . 😅')
        return redirect('community:community_detail', post_id = post.id)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post) #기존 데이터를 가져온 후 POST 데이터로 덮어씌움
        if form.is_valid():
            post = form.save(commit=False)
            form.user = request.user 
            post.modify_date = timezone.now()
            post.save()
            return redirect('community:community_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {'form' : form}
    return render(request, 'community/community_form.html', context)