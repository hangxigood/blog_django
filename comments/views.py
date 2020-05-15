from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.decorators.http import require_POST

from comments.forms import CommentForm
from myblog.models import Post


@require_POST  # 仅 POST 请求可调用该函数
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)  # 取出表单数据，形成表单实例

    if form.is_valid():
        comment = form.save(commit=False)  # 仅生成 Comment 实例，未保存数据库
        comment.post = post
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论成功!', extra_tags='success')
        return redirect(post)

    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论失败！', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)