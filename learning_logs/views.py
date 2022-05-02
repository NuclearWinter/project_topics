from django.shortcuts import render
from .models import Topic


def index(request):
    """Домашняя страница приложения Learing Log"""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """"Выводит список тем"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Выводит тему и связанные записи"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-data_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
