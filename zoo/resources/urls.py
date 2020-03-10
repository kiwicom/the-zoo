from django.urls import include, path

from . import views

urlpatterns = [
    path("libraries/", views.LibraryOverview.as_view(), name="library_overview"),
    path(
        "dependencies/",
        include(
            [
                path(
                    "", views.DependencyOverview.as_view(), name="dependency_overview"
                ),
                path(
                    "<int:pk>/",
                    views.DependencyDetail.as_view(),
                    name="dependency_detail",
                ),
            ]
        ),
    ),
    path(
        "ci_templates/", views.CiTemplateOverview.as_view(), name="ci_template_overview"
    ),
    path(
        "project_templates/",
        views.ProjectTemplateOverview.as_view(),
        name="project_template_overview",
    ),
    path("languages/", views.LanguageOverview.as_view(), name="language_overview"),
]
