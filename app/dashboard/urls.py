from django.urls import path

from .views import (
    DashboardView,
    DataSchemaCreateView,
    DataSchemaDeleteView,
    DataSchemaUpdateView,
    DataSetGenerateView,
    DataSetListView,
    HomeView,
)

app_name = "dashboard"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="index",
    ),
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="home",
    ),
    path(
        "dashboard/schemas/new/",
        DataSchemaCreateView.as_view(),
        name="schema-create",
    ),
    path(
        "dashboard/schemas/<int:pk>/edit/",
        DataSchemaUpdateView.as_view(),
        name="schema-update",
    ),
    path(
        "dashboard/schemas/<int:pk>/delete/",
        DataSchemaDeleteView.as_view(),
        name="schema-delete",
    ),
    path(
        "dashboard/schemas/<int:pk>/datasets/",
        DataSetListView.as_view(),
        name="schema-datasets",
    ),
    path(
        "dashboard/schemas/generate/",
        DataSetGenerateView.as_view(),
        name="schema-generate",
    ),
]
