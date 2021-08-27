#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import resolve, reverse



# Create your views here.

# This commented out code ceates an object and initialize it with the table boards and displays the name column of boards.
# def home(request):
#    boards = Board.objects.all()
#    boards_names = list()
#    boards_desc = list()
#    for board in boards:
#      boards_names.append(board.name)
#    response_html = '<br>'.join(boards_names)
#    return HttpResponse(response_html)


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


#def board_topics(request, board_id):
#   try:
#      board = Board.objects.get(id=board_id)
# except Board.DoesNotExist:
    #    raise Http404
    #return render(request,'topics.html',{'board':board})


#GCBV Implementation of above function plus pagination:
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, id=self.kwargs.get('board_id'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset










@login_required
def new_topic(request, topic_id):
    board  = get_object_or_404(Board, id=topic_id)


    #user = User.objects.first()  # TODO: get the currently logged in user - DONE on Aug 24, 2021!
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', board_id=board.pk, topic_id=topic.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})



#def topic_posts(request, board_id, topic_id):
#    topic = get_object_or_404(Topic, board_id=board_id, id=topic_id)
#    topic.views += 1
#    topic.save()
#    return render(request, 'topic_posts.html', {'topic': topic})

#Above function re-implemented using GCBV and pagination
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
            
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board_id=self.kwargs.get('board_id'), id=self.kwargs.get('topic_id'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset





@login_required
def reply_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, id=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()  
            topic.save()
            topic_url = reverse('topic_posts', kwargs={'board_id': board_id, 'topic_id':topic_id})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )
            
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})




def board_topics(request,board_id):
    board = get_object_or_404(Board, pk=board_id)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})




@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', board_id=post.topic.board.pk, topic_id=post.topic.pk)
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)



