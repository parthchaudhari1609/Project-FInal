from django.contrib import admin
from django.urls import path,include
from . views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [ 
    path("create/",ProjectCreationView.as_view(),name="project_create"),
    path("list/",ProjectListView.as_view(),name="project_list"),
    path("edit/<int:pk>/",ProjectEditView.as_view(),name="project_edit"),
    path("detail/<int:pk>/",ProjectDetailView.as_view(),name="project_detail"),
    path("delete/<int:pk>/",ProjectDeleteView.as_view(),name="project_delete"),
    path("create_team/",ProjectTeamCreateView.as_view(),name="project_team_create") ,
    path("create_status/",ProjectStatusCreateView.as_view(),name="project_status_create"),
    path("create_module/",ProjectModuleCreateView.as_view(),name="module_create"),
    path("list_module/",ProjectModuleListView.as_view(),name="module_list"),
    path("edit_module/<int:pk>",ProjectModuleEditView.as_view(),name="module_edit"),
    path("detail_module/<int:pk>/",ProjectModuleDetailView.as_view(),name="module_detail"),
    path("delete_module/<int:pk>/",ProjectModuleDeleteView.as_view(),name="module_delete"),
    path("create_task/",ProjectTaskCreateView.as_view(),name="task_create"),
    path("list_task/",ProjectTaskListView.as_view(),name="task_list"),
    path("edit_task/<int:pk>",ProjectTaskEditView.as_view(),name="task_edit"),
    path("detail_task/<int:pk>/",ProjectTaskDetailView.as_view(),name="task_detail"),
    path("delete_task/<int:pk>/",ProjectTaskDeleteView.as_view(),name="task_delete"),
    path("assign_task/",AssignTaskView.as_view(),name="assign_task"),
    path('update_task_status/<int:task_id>/', UpdateTaskStatusView.as_view(), name='update_task_status'),
    path('project/<int:project_id>/generate-pdf-report/', generate_pdf_report, name='generate_pdf_report'),
    path('reports/<int:project_id>/', generate_html_report, name='generate_html_report'),


]

