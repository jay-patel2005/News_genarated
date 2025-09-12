from django.shortcuts import render, redirect
from .models import News, Feedback

def home(request):
    query = request.GET.get("q", "")
    if query:
        articles = News.objects.filter(title__icontains=query)
    else:
        articles = News.objects.all().order_by("-published_at")[:10]

    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")
        if name and message:
            Feedback.objects.create(name=name, message=message)
            return redirect("home")

    return render(request, "news/home.html", {"articles": articles, "query": query})
def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        Feedback.objects.create(name=name, message=message)
        return redirect('home')


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import SavedArticle

@login_required
def save_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        url = request.POST.get('url')
        published_at = request.POST.get('published_at')
        SavedArticle.objects.create(
            user=request.user,
            title=title,
            url=url,
            published_at=published_at
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
