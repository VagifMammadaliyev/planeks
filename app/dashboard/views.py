from django import views
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from dataschemas.models import DataColumn, DataSchema, DataSet
from .forms import DataColumnFormSet, DataSchemaForm, GenerateDataSetForm


class HomeView(generic.RedirectView):
    permanent = False
    pattern_name = "dashboard:home"


@method_decorator(login_required, name="dispatch")
class DashboardView(generic.ListView):
    template_name = "dashboard/index.html"
    context_object_name = "dataschemas"

    def get_queryset(self):
        return self.request.user.dataschemas.all().order_by("-id")


class DataSchemaViewMixin:
    success_url = reverse_lazy("dashboard:home")
    form_class = DataSchemaForm
    model = DataSchema
    template_name = "dashboard/schema_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "formset" not in context:
            context["formset"] = self.get_datacolumn_formset(self.request)
        if "form" not in context:
            context["form"] = self.get_dataschema_form(self.request)
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_post_datacolumn_formset(request)
        form = self.get_post_dataschema_form(request)
        if not getattr(self, "object", None):
            self.object = form.instance
        if formset.is_valid() and form.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    @transaction.atomic
    def form_valid(self, form, formset):
        dataschema = form.instance
        dataschema.user = self.request.user
        form.save()
        columns = formset.save(commit=False)
        self.handle_datacolumns(dataschema, columns)
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class DataSchemaCreateView(DataSchemaViewMixin, generic.CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "New data schema"
        return context

    def get_post_dataschema_form(self, request):
        return DataSchemaForm(data=request.POST)

    def get_post_datacolumn_formset(self, request):
        return DataColumnFormSet(data=request.POST)

    def get_datacolumn_formset(self, request):
        return DataColumnFormSet(queryset=DataColumn.objects.none())

    def get_dataschema_form(self, request):
        return DataSchemaForm()

    def handle_datacolumns(self, dataschema, columns):
        for column in columns:
            column.schema = dataschema
        return DataColumn.objects.bulk_create(columns)


@method_decorator(login_required, name="dispatch")
class DataSchemaUpdateView(DataSchemaViewMixin, generic.UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "Edit data schema"
        return context

    def get_object(self):
        return get_object_or_404(self.request.user.dataschemas, pk=self.kwargs["pk"])

    def get_datacolumn_formset(self, request):
        return DataColumnFormSet(queryset=self.object.columns.all().order_by("order"))

    def get_dataschema_form(self, request):
        return DataSchemaForm(instance=self.object)

    def get_post_dataschema_form(self, request):
        return DataSchemaForm(instance=self.object, data=request.POST)

    def get_post_datacolumn_formset(self, request):
        return DataColumnFormSet(data=self.request.POST)

    def handle_datacolumns(self, dataschema, columns):
        # Just remove all columns and create them again...
        # NOTE: This may cause performance issues if dataschema has
        #        lots of columns. For example 10K+! But this solution
        #        is more readable after all.
        dataschema.columns.all().delete()
        for column in columns:
            column.schema = dataschema
        return DataColumn.objects.bulk_create(columns)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        return super().post(*args, **kwargs)


@method_decorator(login_required, name="dispatch")
class DataSchemaDeleteView(generic.DeleteView):
    model = DataSchema
    success_url = reverse_lazy("dashboard:home")
    template_name = "dashboard/schema_delete.html"


@method_decorator(login_required, name="dispatch")
class DataSetListView(generic.ListView):
    template_name = "dashboard/datasets.html"
    context_object_name = "datasets"

    def get(self, *args, **kwargs):
        self.schema = self.get_dataschema()
        return super().get(*args, **kwargs)

    def get_dataschema(self):
        return get_object_or_404(
            self.request.user.dataschemas.all(), pk=self.kwargs["pk"]
        )

    def get_queryset(self):
        return self.schema.datasets.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schema"] = self.get_dataschema()
        context["form"] = GenerateDataSetForm(initial={"schema": context["schema"].id})
        return context

    def get_queryset(self):
        return self.schema.generations.all().order_by("-id")


@method_decorator(login_required, name="dispatch")
class DataSetGenerateView(generic.FormView):
    form_class = GenerateDataSetForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["request"] = self.request
        return form_kwargs

    def form_valid(self, form):
        self.schema = form.cleaned_data["schema"]

        DataSet.objects.create_from_dataschema(
            self.schema, form.cleaned_data["row_count"]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dashboard:schema-datasets", args=(self.schema.id,))
