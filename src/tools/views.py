from django.shortcuts import render


from .models import Category, Tool

def render_tools(request):
    tools = Tool.objects.all()
    categories = Category.objects.all()
    return render(request, 'dashboard/partials/_tools_.html', {'tools': tools, 'categories': categories})
    

def tools(request):
    categories = Category.objects.all()
    print(categories)
    return render(request, 'dashboard/tools.html', {'categories': categories})



def filter(request, category_id):
    category = Category.objects.get(id=category_id)
    tools = Tool.categories.all()
    return render(request, 'dashboard/partials/__tools__.html', {'categories':category, 'tools':tools})
