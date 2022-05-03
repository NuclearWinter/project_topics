
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """Домашняя страница приложения Learing Log"""
    return render(request, 'app_topics/index.html')

@login_required
def topics(request):
    """"Выводит список тем"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'app_topics/topics.html', context)

@login_required
def topic(request, topic_id):
    """Выводит тему и связанные записи"""
    topic = Topic.objects.get(id=topic_id)
    # Проверка, что тема принадлежит текущему пользователю
    check_topic_owner(topic, request.user)

    entries = topic.entry_set.order_by('-data_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'app_topics/topic.html', context)


def check_topic_owner(topic, current_user):
    if topic.owner != current_user:
        raise Http404


@login_required
def new_topic(request):
    """Новая тема"""
    if request.method != 'POST':
        # Данные не отправлялись, создается пустая форма
        form = TopicForm()
    else:
        # Отправлены данные POST, обработать данные
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('app_topics:topics')

    # Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'app_topics/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """"Добавляет новую запись по конкретной теме"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request.user)
    if request.method != 'POST':
        # Данные не отправлялись, создается пустая форма
        form = EntryForm()
    else:
        # Отправлен POST запрос, обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('app_topics:topic', topic_id)

    # Вывести пустую или недействительную форму
    context = {'topic': topic, 'form': form}
    return render(request, 'app_topics/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """"Редактирует существующую запись"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request.user)

    if request.method != 'POST':
        # Исходный запрос, форма заполняется данными текущей записи
        form = EntryForm(instance=entry)
    else:
        # Отправлен POST запрос, обработать данные
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_topics:topic', topic.id)

    context = {
        'entry': entry,
        'topic': topic,
        'form': form,
    }
    return render(request, 'app_topics/edit_entry.html', context)
