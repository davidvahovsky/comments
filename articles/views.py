import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from articles.models import Article, Comment
from django.views.generic.list import ListView


class ArticleDetailView(TemplateView):

    template_name = 'articles/article_detail.html'

    def get_context_data(self, **kwargs):
        try:
            article = Article.objects.get(id=self.kwargs['pk'])
            articles = Article.objects.all()
            total_comments = len(Comment.objects.filter(article_id=article.id))
            context = super(ArticleDetailView, self).get_context_data(**kwargs)
            context['article'] = article
            context['articles'] = articles
            context['articles_len'] = len(articles)
            context['total_comments'] = total_comments
            return context
        except Article.DoesNotExist:
            return HttpResponseRedirect(reverse('article_list'))


class CommentLikeView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        comment.likes += 1
        comment.save()
        return self.request.META['HTTP_REFERER']


class CommentDislikeView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        comment.likes -= 1
        comment.save()
        return self.request.META['HTTP_REFERER']


class CommentListView(ListView):
    model = Comment
    template_name = "articles/comment_list.html"
    context_object_name = "comment_list"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        try:
            article = Article.objects.get(id=self.kwargs['pk'])
        except Article.DoesNotExist:
            article = None
        context = super(CommentListView, self).get_context_data(**kwargs)
        comment_list = Comment.objects.filter(comment_id__isnull=True, article_id=self.kwargs['pk']).order_by("-likes")
        # comment_list = Comment.objects.filter(comment_id__isnull=True, article_id=self.kwargs['pk']).order_by("-date_created")
        paginator = Paginator(comment_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            comment_file = paginator.page(page)
        except PageNotAnInteger:
            comment_file = paginator.page(1)
        except EmptyPage:
            comment_file = paginator.page(paginator.num_pages)

        if int(page) > int(paginator.num_pages):
            raise Http404
        context['comment_list'] = comment_file
        context['page'] = int(page)
        context['article'] = article
        return context


class SubCommentListView(ListView):
    model = Comment
    template_name = "articles/sub_comment_list.html"
    context_object_name = "comment_list"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        try:
            article = Article.objects.get(id=self.kwargs['pk'])
        except Article.DoesNotExist:
            article = None
        try:
            parent_comment = Comment.objects.get(id=self.kwargs['com_pk'])
        except Comment.DoesNotExist:
            parent_comment = None
        context = super(SubCommentListView, self).get_context_data(**kwargs)
        comment_list = Comment.objects.filter(comment_id=self.kwargs['com_pk'], article_id=self.kwargs['pk']).order_by("-likes")
        # comment_list = Comment.objects.filter(comment_id=self.kwargs['com_pk'], article_id=self.kwargs['pk']).order_by("-date_created")
        paginator = Paginator(comment_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            comment_file = paginator.page(page)
        except PageNotAnInteger:
            comment_file = paginator.page(1)
        except EmptyPage:
            comment_file = paginator.page(paginator.num_pages)

        if int(page) > int(paginator.num_pages):
            raise Http404
        context['comment_list'] = comment_file
        context['page'] = int(page)
        context['article'] = article
        context['parent_comment'] = parent_comment
        return context


def add_form(request, pk, com_pk):
    try:
        article = Article.objects.get(id=pk)
        try:
            parent_comment = Comment.objects.get(id=com_pk)
            return render_to_response('articles/add_subcomment.html',
                                      {'pk': pk, 'article': article, 'parent_comment': parent_comment})
        except Comment.DoesNotExist:
            return request.META['HTTP_REFERER']
    except Article.DoesNotExist:
        return request.META['HTTP_REFERER']


@csrf_exempt
def comment_create(request, pk):
    try:
        article = Article.objects.get(id=pk)
        if request.method == 'POST':
            post_nick = request.POST.get('nick')
            post_body = request.POST.get('body')
            if not post_nick:
                return request.META['HTTP_REFERER']
            if not post_body:
                return request.META['HTTP_REFERER']
            comment = Comment(nick=post_nick, body=post_body, article=article)
            comment.save()
            return render_to_response('articles/comment_detail.html',
                                      {'pk': pk, 'nick': post_nick, 'body': post_body, 'article': article,
                                       'item': comment})
        else:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )
    except Article.DoesNotExist:
        return request.META['HTTP_REFERER']


@csrf_exempt
def subcomment_create(request, pk, com_pk):
    try:
        article = Article.objects.get(id=pk)
        try:
            parent_comment = Comment.objects.get(id=com_pk)
            if request.method == 'POST':
                post_nick = request.POST.get('nick')
                post_body = request.POST.get('body')
                if not post_nick:
                    return request.META['HTTP_REFERER']
                if not post_body:
                    return request.META['HTTP_REFERER']
                comment = Comment(nick=post_nick, body=post_body, article=article, comment=parent_comment)
                comment.save()
                return render_to_response('articles/comment_detail.html',
                                          {'pk': pk, 'nick': post_nick, 'body': post_body, 'article': article,
                                           'parent_comment': parent_comment, 'item': comment})
            else:
                return HttpResponse(
                    json.dumps({"nothing to see": "this isn't happening"}),
                    content_type="application/json"
                )
        except Comment.DoesNotExist:
            return request.META['HTTP_REFERER']
    except Article.DoesNotExist:
        return request.META['HTTP_REFERER']