from django.db import models
from user.models import User
# Create your models here.
techChoices = (
    ("Python", "Python"),
    ("Java", "Java"),
    ("C++", "C++"),
    ("C#", "C#"),
)
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=100,choices=techChoices)
    estimated_hours = models.PositiveIntegerField()
    startDate = models.DateField()
    endDate = models.DateField()

    class Meta:
        db_table = "project"
    
    def __str__(self): 
        return self.name

class ProjectTeam(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "projectteam"
    
    def __str__(self):
        return self.user.username

class Status(models.Model):
    status_name = models.CharField(max_length=100)

    class Meta:
        db_table = "status"
    
    def __str__(self):
        return self.status_name

class ProjectModule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    moduleName = models.CharField(max_length=100)
    description = models.TextField()
    estimatedMinutes = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    startDate = models.DateField()
    totalUtilMinutes = models.IntegerField()

    class Meta:
        db_table = "project_module"
    
    def __str__(self) -> str:
        return self.moduleName
priorityChoice = (
    ("High","High"),
    ("Medium","Medium"),
    ("Low","Low"),
)
class Task(models.Model):
    module = models.ForeignKey(ProjectModule, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    priority = models.CharField(max_length=100,choices=priorityChoice)
    description = models.TextField()
    estimatedMinutes = models.IntegerField()
    totalUtilMinutes = models.IntegerField()

    class Meta:
        db_table = "task"

    def __str__(self):
        return self.task_name

class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    totalUtilMinutes = models.IntegerField()

    class Meta:
        db_table = "user_task"

        
class Badge(models.Model):
    badge = models.CharField(max_length=100)

    class Meta:
        db_table = "badge"



class TaskBadge(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        db_table = "task_badge"



