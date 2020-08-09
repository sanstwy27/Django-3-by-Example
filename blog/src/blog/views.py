from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm


# FBV
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3) # 3 Article per Page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Default go to Page 1
        posts = paginator.page(1)
    except EmptyPage:
        # Exceed Range
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month,
                             publish__day=day)
    # List all comments of the Post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # New Comment Instance
            new_comment = comment_form.save(commit=False)
            # Set The Post as Foreign-Key
            new_comment.post = post
            # Save to DB
            new_comment.save()
    else:
        comment_form = CommentForm()
    # Similar Articles
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_tags = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


def post_share(request, post_id):
    # Get id from Post Objecct
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == "POST":
        # Form Submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Verify Data
            cd = form.cleaned_data
            # Send Mail
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, '***************', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # -- Exact searching --
            #search_query = SearchQuery(query)
            #search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            #results = Post.objects.annotate(search=search_vector,
            #                        rank=SearchRank(search_vector, search_query)
            #                        ).filter(rank__gte=0.3).order_by('-rank')
            # -- Fuzzy searching --
            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gte=0.1).order_by('-similarity')
    return render(request, 'blog/post/search.html', {'query': query, "form": form, 'results': results})

# CBV
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'