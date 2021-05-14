from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Tag, Post, Category
from config.models import SiderBar
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from comment.forms import CommentFor
from comment.models import Comment

# class-based view 写法


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SiderBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_post()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """重写queryset,根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get("tag_id")
        tag = get_object_or_404(Category, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset,根据分类过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_post()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form': CommentFor,
            'comment_list': Comment.get_by_target(self.request.path),
        })
        return context

class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
   def get_queryset(self):
       queryset = super().get_queryset()
       author_id = self.kwargs.get('owner_id')
       return queryset.filter(owner_id=author_id)

# -------------------------------------------function VIEW写

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
