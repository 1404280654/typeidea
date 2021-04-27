from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Tag, Post, Category
from config.models import SiderBar
# Create your views here.


def post_list(request, category_id=None, tag_id=None):
    """
    :param request:
    :param category_id:
    :param tag_id:


        content = 'post_list category_id={category_id}, tag_id={tag_id}'.format(
        category_id=category_id,
        tag_id=tag_id,
    )
    # 括号内直接跟一个具体的字符串作为响应体
    return HttpResponse(content)
    """
    # def render(request, template_name, context=None, content_type=None, status=None, using=None):
    # template_name:模板名称，页面代码路径，contex:字典数据传输， content_type,页面编码，默认text/html,
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category =Post.get_by_category(category_id)
    else:
        post_list = Post.latest_post()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SiderBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post': post})
