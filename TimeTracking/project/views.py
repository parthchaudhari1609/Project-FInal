from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from . forms import *
from . models import *
from user.models import User
from django.shortcuts import get_object_or_404
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect, reverse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.styles import * 
# Create your views here.
class ProjectCreationView(CreateView):
    template_name = "project/create.html"
    model = Project
    form_class = ProjectCreationForm
    success_url = "/project/list"

class ProjectListView(ListView):
    template_name = "project/list.html"
    model = Project
    context_object_name = "projects"

class ProjectEditView(UpdateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = "project/edit.html"
    success_url = "/project/list"

class ProjectDetailView(DetailView):
    model = Project
    template_name = "project/detail.html"
    context_object_name = "project"

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "project/delete.html"
    success_url = "/project/list"

class ProjectTeamCreateView(CreateView):
    template_name = "project/create_team.html"
    model = ProjectTeam
    success_url = "/project/list/"
    form_class = ProjectTeamCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_id = self.request.GET.get('project_id')
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            kwargs['initial']['project'] = project
        return kwargs
    
class ProjectStatusCreateView(CreateView):
    template_name = "project/status.html"
    model = Status
    success_url = "/project/list"
    form_class = ProjectStatusCreationForm

class ProjectModuleCreateView(CreateView):
    template_name = "project/create_module.html"
    model = ProjectModule
    success_url = "/project/list"
    form_class = ProjectModuleCreationForm

    # def get_form(self):
    #     form = super().get_form()
    #     form.fields['startDate'].widget = DateTimePickerInput()
    #     return form
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_id = self.request.GET.get('project_id')
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            kwargs['initial']['project'] = project
        return kwargs
    
class ProjectModuleListView(ListView):
    template_name = "project/list_module.html"
    model = ProjectModule
    context_object_name = "modules"

class ProjectModuleEditView(UpdateView):
    model = ProjectModule
    form_class = ProjectModuleCreationForm
    template_name = "project/edit_module.html"
    success_url = "/project/list"

class ProjectModuleDetailView(DetailView):
    model = ProjectModule
    template_name = "project/detail_module.html"
    context_object_name = "module"

class ProjectModuleDeleteView(DeleteView):
    model = ProjectModule
    template_name = "project/delete_module.html"
    success_url = "/project/list"

class ProjectTaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = ProjectTaskCreationForm
    template_name = "project/create_task.html"
    success_url = "/project/list"

    def form_valid(self, form):
        if self.request.user.is_manager:
            return super().form_valid(form)
        else:
            raise PermissionDenied("You are not authorized to create tasks.")


class ProjectTaskListView(ListView):
    template_name = "project/list_task.html"
    model = Task
    context_object_name = "task"

class ProjectTaskEditView(UpdateView):
    model = Task
    form_class = ProjectTaskCreationForm
    template_name = "project/edit_task.html"
    success_url = "/project/list"

class ProjectTaskDetailView(DetailView):
    model = Task
    template_name = "project/detail_task.html"
    context_object_name = "task"

class ProjectTaskDeleteView(DeleteView):
    model = Task
    template_name = "project/delete_task.html"
    success_url = "/project/list"

class AssignTaskView(CreateView):
    form_class = TaskAssignForm
    template_name = "project/task_assign.html"
    success_url = "/user/manager-dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter users to only include developers
        developers = User.objects.filter(is_developer=True)
        context['form'].fields['user'].queryset = developers
        return context

    def form_valid(self, form):
        # Send email to the assigned developer
        assigned_user = form.cleaned_data.get("user")
        task_name = form.cleaned_data.get("task")
        total_util_minutes = form.cleaned_data.get("totalUtilMinutes")

        subject = "New Task Assigned"
        message = f"Hello {assigned_user.username},\n\n"
        message += f"We're excited to inform you that you've been assigned a new task:\n\n"
        message += f"Task: {task_name}\n"
        message += f"Estimated Completion Time: {total_util_minutes} minutes\n\n"
        message += "For more details, please check your dashboard.\n\n"

        recepient = [assigned_user.email]
        EMAIL_FROM = settings.EMAIL_HOST_USER

        send_mail(subject, message, EMAIL_FROM, recepient)

        # Call the parent's form_valid method to save the form
        return super().form_valid(form)
    

class UpdateTaskStatusView(View):
   def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        current_status = task.status

        # Define the logic for moving to the next status
        if current_status.status_name == 'Not Started':
            next_status_name = 'In-Progress'
        elif current_status.status_name == 'In-Progress':
            next_status_name = 'Testing'
        elif current_status.status_name == 'Testing':
            next_status_name = 'Complete'
        else:
            # If the task is already in the last status, no change needed
            return redirect('developer-dashboard')  

        try:
            next_status = Status.objects.get(status_name=next_status_name)
            task.status = next_status
            task.save()
        except Status.DoesNotExist:
            # Handle the case where the next status doesn't exist
            pass
        
        return redirect('developer-dashboard') 

def generate_pdf_report(request, project_id): 

    # Fetch project, modules, tasks, and developers from the database
    project = Project.objects.get(id=project_id)
    modules = ProjectModule.objects.filter(project=project)
    tasks = Task.objects.filter(project=project)
    project_teams = ProjectTeam.objects.filter(project=project)

    # Fetch project manager
    project_manager = project_teams.filter(user__is_manager=True).first()

    # Fetch developers working on the project
    developers = project_teams.exclude(user__is_manager=True)

    # Create a buffer to store the PDF
    buffer = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    # Define data for the PDF report
    data = []

    # Add project report title
    data.append([Paragraph('Project Report', title_style)])
    data.append([])

    # Add project manager
    if project_manager:
        project_manager_name = project_manager.user.get_full_name()
        data.append([Paragraph('Project Manager:', heading_style), project_manager_name])
        data.append([])

    # Add developers
    developer_names = [team.user.get_full_name() for team in developers]
    if developer_names:
        data.append([Paragraph('Developers working on project:', heading_style)])
        for name in developer_names:
            data.append([name])
        data.append([])

    # Add modules
    data.append([Paragraph('Modules:', heading_style), ''])
    data.append([
        Paragraph('Module', body_style),
        Paragraph('Description', body_style),
        Paragraph('Status', body_style)
    ])
    for module in modules:
        data.append([
            module.moduleName,
            module.description,
            module.status.status_name
        ])
    data.append([])

    # Add tasks
    data.append([Paragraph('Tasks:', heading_style), ''])
    data.append([
        Paragraph('Task Name', body_style),
        Paragraph('Status', body_style),
        
    ])
    for task in tasks:
        data.append([
            task.task_name,
            task.status.status_name,
        ])

    # Create a table with the data
    table = Table(data)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Build PDF document
    doc.build([table])  # Pass table as a list

    # Get the value of the buffer and create the response
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="project_report_{project_id}.pdf"'
    response.write(pdf)
    return response


def generate_html_report(request, project_id):
    project = Project.objects.get(id=project_id)
    modules = ProjectModule.objects.filter(project=project)
    tasks = Task.objects.filter(project=project)
    project_teams = ProjectTeam.objects.filter(project=project)


    # Fetch developers working on the project
    developers = [team.user.get_full_name() for team in project_teams.exclude(user__is_manager=True)]

    context = {
        'project': project,
        'developers': developers,
        'modules': modules,
        'tasks': tasks
    }
    return render(request, 'project/project_status_report.html', context)