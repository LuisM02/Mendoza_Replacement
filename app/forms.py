from .models import Material, Project, ProjectElement
from datetime import date, timezone
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )


from django import forms
from .models import Material, ProjectElement


class MaterialForm(forms.ModelForm):
    ELEMENT_MATERIAL_CHOICES = {
        "Framing": [
            ("Exterior Wall Framing", "Exterior Wall Framing"),
            ("Roof Framing", "Roof Framing"),
            ("Door Framing", "Door Framing"),
        ],
        "Window and Door Installation": [
            ("Barn Door", "Barn Door"),
            ("Sliding Door", "Sliding Door"),
        ],
        "Electrical": [
            ("Light Switches", "Light Switches"),
            ("Main Panel", "Main Panel"),
        ],
        "Plumbing": [
            ("Shower Fixture", "Shower Fixture"),
            ("Toilet Installation", "Toilet Installation"),
        ],
    }

    name = forms.ChoiceField(
        choices=[], widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Material
        fields = ["name", "quantity", "unit", "price_per_qty", "markup_percentage"]

        widgets = {
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit": forms.TextInput(attrs={"class": "form-control"}),
            "price_per_qty": forms.NumberInput(attrs={"class": "form-control"}),
            "markup_percentage": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        element = kwargs.pop("element", None)
        super().__init__(*args, **kwargs)

        if element and element.name in self.ELEMENT_MATERIAL_CHOICES:
            self.fields["name"].choices = self.ELEMENT_MATERIAL_CHOICES[element.name]
        else:
            self.fields["name"].choices = []


class ProjectElementForm(forms.ModelForm):
    ELEMENT_CHOICES = [
        ("Framing", "Framing"),
        ("Window and Door Installation", "Window and Door Installation"),
        ("Electrical", "Electrical"),
        ("Plumbing", "Plumbing"),
    ]

    name = forms.ChoiceField(
        choices=ELEMENT_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = ProjectElement
        fields = ["name"]


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "location", "status"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        project = super().save(commit=False)
        if project.status == "completed" and not project.end_date:
            project.end_date = timezone.now().date()
        if commit:
            project.save()
        return project


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get("password") == cleaned_data.get("confirm_password")):
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class RequestQuoteForm(forms.Form):
    ELEMENT_CHOICES = [
        ("Framing", "Framing"),
        ("Window and Door Installation", "Window and Door Installation"),
        ("Electrical", "Electrical"),
        ("Plumbing", "Plumbing"),
    ]

    MATERIAL_CHOICES = [
        ("Exterior Wall Framing", "Exterior Wall Framing"),
        ("Roof Framing", "Roof Framing"),
        ("Door Framing", "Door Framing"),
        ("Barn Door", "Barn Door"),
        ("Sliding Door", "Sliding Door"),
        ("Light Switches", "Light Switches"),
        ("Main Panel", "Main Panel"),
        ("Shower Fixture", "Shower Fixture"),
        ("Toilet Installation", "Toilet Installation"),
    ]

    area_size = forms.DecimalField(
        label="Area Size (sq.m)",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter area size in sq.m"}
        ),
    )
    project_elements = forms.ChoiceField(
        choices=ELEMENT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check"}),
        label="Choose Project Elements",
    )
    materials = forms.MultipleChoiceField(
        choices=MATERIAL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check"}),
        label="Choose Materials",
    )

    class Meta:
        fields = ["area_size", "project_elements", "materials"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "project_elements" in self.data:
            try:
                element_id = int(self.data.get("project_elements"))
                self.fields["materials"].queryset = Material.objects.filter(
                    element_id=element_id
                )
            except (ValueError, TypeError):
                pass

    def save(self, user):
        project = Project.objects.create(
            user=user,
            description="Quotation requested project",
            location="Location unspecified",
            created_at=date.today(),
            status="pending",
        )

        project_element = ProjectElement.objects.create(
            project=project, name=self.cleaned_data["project_elements"]
        )

        selected_materials = self.cleaned_data["materials"]
        for material_name in selected_materials:
            Material.objects.create(
                element=project_element,
                name=material_name,
                quantity=1,
                unit="pcs",
                price_per_qty=100.00,
                markup_percentage=10.0,
            )

        project.save()
        return project
