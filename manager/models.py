from django.db import models
from django.contrib.auth.models import User
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Create your models here.
class User_Project(models.Model):
    name = models.CharField(max_length=150)
    user = models.CharField(max_length = 300, default='def')

class Project(models.Model):
    name = models.CharField(max_length=150)
    
 

class Task(models.Model):
    name = models.CharField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, default='')
    due = models.CharField(max_length=200, default="2021-01-17")
    status = models.CharField(max_length=200, default='Incomplete')
    archived = models.BooleanField(default=False)

    def values(self):
        out =   {
            'name' : self.name,
            'project' : self.project.name,
            'type' : self.type,
            'due':self.due,
            'status':self.status,
            'archived':self.archived,
        }
        return out

class TextField(models.Model):
    type = models.CharField(max_length=150)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    value = models.CharField(max_length= 500)

class NumberField(models.Model):
    type = models.CharField(max_length=150)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    value = models.CharField(max_length= 500)

class SelectField(models.Model):
    type = models.CharField(max_length=150)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    value = models.CharField(max_length= 500)

