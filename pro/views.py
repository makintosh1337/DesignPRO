from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request, Categorys
from .forms import RequestForm, CategoryForm


def index(request):
    completed_requests = Request.objects.filter(status='completed').order_by('-created_at')[:4]
    in_progress_count = Request.objects.filter(status='in_progress').count()
    return render(request, 'index.html', {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count
    })

@login_required
def my_requests(request):
    user_requests = Request.objects.filter(user=request.user)
    status_filter = request.GET.get('status')

    if status_filter == 'new':
        user_requests = user_requests.filter(status='new')
    elif status_filter == 'in_progress':
        user_requests = user_requests.filter(status='in_progress')
    elif status_filter == 'completed':
        user_requests = user_requests.filter(status='completed')

    context = {
        'requests': user_requests
    }
    return render(request, 'my_requests.html', context)

@login_required
def request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('my_requests')
    else:
        form = RequestForm()

    return render(request, 'request.html', {'form': form})

def logins(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/sign.html', {'form': form})


@staff_member_required
def managecategories(request):
    categories = Categorys.objects.all()
    return render(request, 'managecategories.html', {'categories': categories})




@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('managecategories')
    else:
        form = CategoryForm()
    return render(request, 'addcategory.html', {'form': form})

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Categorys, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('managecategories')
    return render(request, 'delete_category.html', {'category': category})

@login_required
def panale(request):
    user_role = 'Администратор' if request.user.is_staff else 'Пользователь'
    return render(request, 'panale.html', {
        'user_role': user_role
    })

@staff_member_required
def status(request, pk):
    request_obj = get_object_or_404(Request, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status == 'in_progress':
            request_obj.status = 'in_progress'
            request_obj.save()
            return redirect('managerequests')
        elif new_status == 'completed':
            if 'completed_image' in request.FILES:
                request_obj.status = 'completed'
                request_obj.image = request.FILES['completed_image']
                request_obj.save()
                return redirect('managerequests')
            else:
                return render(request, 'status.html', {
                    'request_obj': request_obj,
                    'error': 'Для статуса «Выполнено» необходимо прикрепить изображение.'
                })

    return render(request, 'status.html', {
        'request_obj': request_obj
    })


@staff_member_required
def managerequests(request):
    requests = Request.objects.all().order_by('-created_at')
    return render(request, 'managerequests.html', {'requests': requests})


@login_required
def delete_request(request, pk):
    request_obj = get_object_or_404(Request, pk=pk, user=request.user)

    if request.method == 'POST':
        request_obj.delete()
        return redirect('my_requests')

    return redirect('my_requests')
