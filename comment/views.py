from django.shortcuts import render

from blog.models import Post
from blog.views import CommonViewMixin
from comment.forms import CommentFor
from comment.models import Comment
from django.views.generic import DetailView, TemplateView
from django.shortcuts import redirect


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentFor(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False
        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target,
        }
        return self.render_to_response(context)
