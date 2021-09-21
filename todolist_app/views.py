from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    #return HttpResponse("welcome to task page")
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request,("New task added!"))
        return redirect('todolist')
    else:
        all_tasks =  TaskList.objects.filter(manage=request.user)    #fetch data
        paginator = Paginator(all_tasks, 7)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)

        return render(request, 'todolist.html', {'all_tasks': all_tasks})  #{}content

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request,("Access Restricted, You Are Not Allowed!"))
    return redirect('todolist')

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
            form.save()

        messages.success(request,("Tas Edited!"))
        return redirect('todolist')
    else:
        task_obj =  TaskList.objects.get(pk=task_id)    #fetch data
        return render(request, 'edit.html', {'task_obj': task_obj})

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request,("Access Restricted, You Are Not Allowed!"))
    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todolist')

def index(request):
    context = {
        'index_text':"Welcome to Index page",
    }
    return render(request, 'index.html',context)

def contact(request):
    context = {
        'contact_text':"Welcome to Contact page",
    }
    return render(request, 'contact.html',context)

def about(request):
    context = {
        'about_text':"Welcome to About page",
    }
    return render(request, 'about.html',context)
