from django.shortcuts import render
from .models import Tweet, Comments
from .forms import TweetForm, UserRegistrationForm, EditForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all()
    return render(request, 'tweet_list.html', {'tweets' : tweets})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk= tweet_id, user = request.user)
    if(request.method == 'POST'):
        form = TweetForm(request.POST, request.FILES, instance= tweet)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user)
    if(request.method == 'POST'):
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_delete_confirmation.html', {'tweet': tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

def seacrh_tweets(request):
    query = request.GET.get('query', '')
    results = Tweet.objects.filter(text__icontains = query)
    return render(request, 'search_tweet.html', {'results': results, 'query' : query})

def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id)
    comments = tweet.comments.all().order_by('-created_at')
    return render(request, 'tweet_detail.html', {'tweet' : tweet,
                                                 'comments': comments})
@login_required   
def add_comment(request, tweet_id):
    if request.method == 'POST':
        tweet = get_object_or_404(Tweet, pk = tweet_id)
        text = request.POST.get('text')
        Comments.objects.create(tweet = tweet, user = request.user, text = text)
    return redirect('tweet_detail', tweet_id)

def profile_view(request, username):
    user = get_object_or_404(User, username = username)
    results = Tweet.objects.filter(user = request.user)
    return render(request, 'profile_detail.html', {'user': user,
                                                   'tweets': results})

def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', request.user.username)
    else:
        form = EditForm(instance=profile)
    return render(request, 'profile_edit.html', {'form':form})        