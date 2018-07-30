from django.shortcuts import render


from .models import Category, Tool

def render_tools(request):
    tools = Tool.objects.all()
    categories = Category.objects.all()
    return render(request, 'dashboard/partials/_tools_.html', {'tools': tools, 'categories': categories})
    

def tools(request):
    categories = Category.objects.all()
    print(categories)
    tools = Tool.objects.all()
    return render(request, 'dashboard/tools.html', {'tools': tools,'categories': categories})



def filter(request, category_id):
    category = Category.objects.get(id=category_id)
    tools = Tool.objects.filter(categories=category)
    return render(request, 'dashboard/partials/_tools_filter.html', {'categories':category, 'tools':tools})



def map(request):
    return render(request, 'map.html')
