from django.shortcuts import render

# Create your views here.


def repos(request):

    return render(request, 'dashboard/github-repos.html', )


def eos_911(request):

    return render(request, 'dashboard/911.html')


def news(request):

    return render(request, 'dashboard/news.html', )


def youtube(request):

    return render(request, 'dashboard/youtube.html',)


def testnets(request):

    return render(request, 'dashboard/testnets.html', )


def steem(request):

    return render(request, 'dashboard/steem.html',)


def twitter(request):

    return render(request, 'dashboard/twitter.html',)
