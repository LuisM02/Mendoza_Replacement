from .forms import LoginForm, ProjectUpdateForm, RegisterForm, RequestQuoteForm
from .models import Material, Project, ProjectElement
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.
def login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("project_list")
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "app/login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("login")


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    total_cost = 0
    form = None

    if request.user.is_superuser:
        if request.method == "POST":
            form = ProjectUpdateForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                return redirect("project_detail", pk=project.pk)
        else:
            form = ProjectUpdateForm(instance=project)

    for element in project.elements.all():
        for material in element.materials.all():
            total_cost = material.total_cost()

    return render(
        request,
        "app/project_detail.html",
        {"project": project, "total_cost": round(total_cost, 2), "form": form},
    )


@login_required
def project_list(request):
    project = {
        "pending": [],
        "approved": [],
        "declined": [],
        "completed": [],
    }

    if request.user.is_superuser:
        project["pending"] = Project.objects.filter(status="pending")
        project["approved"] = Project.objects.filter(status="approved")
        project["declined"] = Project.objects.filter(status="declined")
        project["completed"] = Project.objects.filter(status="completed")
    else:
        project["pending"] = Project.objects.filter(user=request.user, status="pending")
        project["approved"] = Project.objects.filter(
            user=request.user, status="approved"
        )
        project["declined"] = Project.objects.filter(
            user=request.user, status="declined"
        )
        project["completed"] = Project.objects.filter(
            user=request.user, status="completed"
        )

    print(project)

    return render(request, "app/project_list.html", {"project": project})


@login_required
def project_list_approved(request):
    project = {
        "pending": [],
        "approved": [],
        "declined": [],
        "completed": [],
    }

    if request.user.is_superuser:
        project["pending"] = Project.objects.filter(status="pending")
        project["approved"] = Project.objects.filter(status="approved")
        project["declined"] = Project.objects.filter(status="declined")
        project["completed"] = Project.objects.filter(status="completed")
    else:
        project["pending"] = Project.objects.filter(user=request.user, status="pending")
        project["approved"] = Project.objects.filter(
            user=request.user, status="approved"
        )
        project["declined"] = Project.objects.filter(
            user=request.user, status="declined"
        )
        project["completed"] = Project.objects.filter(
            user=request.user, status="completed"
        )

    print(project)

    return render(request, "app/approved.html", {"project": project})


@login_required
def project_list_declined(request):
    project = {
        "pending": [],
        "approved": [],
        "declined": [],
        "completed": [],
    }

    if request.user.is_superuser:
        project["pending"] = Project.objects.filter(status="pending")
        project["approved"] = Project.objects.filter(status="approved")
        project["declined"] = Project.objects.filter(status="declined")
        project["completed"] = Project.objects.filter(status="completed")
    else:
        project["pending"] = Project.objects.filter(user=request.user, status="pending")
        project["approved"] = Project.objects.filter(
            user=request.user, status="approved"
        )
        project["declined"] = Project.objects.filter(
            user=request.user, status="declined"
        )
        project["completed"] = Project.objects.filter(
            user=request.user, status="completed"
        )

    print(project)

    return render(request, "app/completed.html", {"project": project})


@login_required
def project_list_completed(request):
    project = {
        "pending": [],
        "approved": [],
        "declined": [],
        "completed": [],
    }

    if request.user.is_superuser:
        project["pending"] = Project.objects.filter(status="pending")
        project["approved"] = Project.objects.filter(status="approved")
        project["declined"] = Project.objects.filter(status="declined")
        project["completed"] = Project.objects.filter(status="completed")
    else:
        project["pending"] = Project.objects.filter(user=request.user, status="pending")
        project["approved"] = Project.objects.filter(
            user=request.user, status="approved"
        )
        project["declined"] = Project.objects.filter(
            user=request.user, status="declined"
        )
        project["completed"] = Project.objects.filter(
            user=request.user, status="completed"
        )

    print(project)

    return render(request, "app/completed.html", {"project": project})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "app/register.html", {"form": form})


@login_required
def request_quote(request):
    if request.method == "POST":
        form = RequestQuoteForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
    else:
        form = RequestQuoteForm()
    return render(request, "app/request_quote.html", {"form": form})


@login_required
def update_element(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = None

    return render(
        request, "app/update_element.html", {"project": project, "form": form}
    )


@login_required
def update_material(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = None

    return render(
        request, "app/update_element.html", {"project": project, "form": form}
    )


"""
    Request
"""
