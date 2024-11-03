from .forms import (
    LoginForm,
    MaterialForm,
    MaterialUpdateForm,
    ProjectElementForm,
    ProjectUpdateForm,
    RegisterForm,
    RequestQuoteForm,
)
from .models import Material, Project, ProjectElement
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.
@login_required
def delete_project_element(request, element_id):
    element = get_object_or_404(ProjectElement, id=element_id)
    project_id = element.project.id
    element.delete()
    return redirect("project_detail", project_id=project_id)


@login_required
def delete_project_element_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    project_id = material.element.project.id
    material.delete()
    return redirect("project_detail", project_id=project_id)


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
            total_cost += material.total_cost()

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

    if request.method == "POST":
        form = ProjectElementForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            element.project = project
            element.save()
            return redirect("project_detail", project_id=project.pk)
    else:
        form = ProjectElementForm()

    return render(
        request, "app/update_element.html", {"project": project, "form": form}
    )


@login_required
def update_material(request, project_id, element_id):
    project = get_object_or_404(Project, pk=project_id)
    element = get_object_or_404(ProjectElement, pk=element_id)
    form = None

    if request.method == "POST":
        form = MaterialForm(request.POST, element=element)
        if form.is_valid():
            material = form.save(commit=False)
            material.element = element
            material.save()
            return redirect("element_detail", project_id=element_id)
    else:
        form = MaterialForm(element=element)

    return render(
        request,
        "app/update_material.html",
        {"element": element, "project": project, "form": form},
    )


@login_required
def update_material_detail(request, project_id, element_id, material_id):
    project = get_object_or_404(Project, pk=project_id)
    element = get_object_or_404(ProjectElement, pk=element_id)
    material = get_object_or_404(Material, pk=material_id)

    if request.method == "POST":
        form = MaterialUpdateForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = MaterialUpdateForm(instance=material)

    return render(
        request, "app/update_material_detail.html", {"form": form, "material": material}
    )


@login_required
def update_status_approved(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.status = "approved"

    return redirect("project_detail", project_id=project.id)


@login_required
def update_status_declined(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.status = "declined"

    return redirect("project_detail", project_id=project.id)


@login_required
def update_status_completed(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.status = "completed"

    return redirect("project_detail", project_id=project.id)


"""
    Request
"""
