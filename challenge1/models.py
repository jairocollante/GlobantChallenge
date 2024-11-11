from django.db import models

class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    department = models.CharField(max_length=200)     # Name of the department
    
    def __str__(self):
        return f"Department {self.id} - {self.department}"


class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    job = models.CharField(max_length=200)     # Name of the job
    
    def __str__(self):
        return f"Job {self.id} - {self.job}"


class Hiredemployee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)     #Name and surname of the employee
    datetime = models.DateTimeField()           #Hire datetime in ISO format
    department = models.ForeignKey(Department, on_delete=models.CASCADE)       #Id of the department which the employee was hired for
    job = models.ForeignKey(Job, on_delete=models.CASCADE)              #Id of the job which the employee was hired for

    def __str__(self):
        return f"Hired_employees {self.id} - {self.name}"


class Logger(models.Model):
    detail = models.TextField()  
    log = models.TextField()     
    save_date = models.DateTimeField(auto_now=True)


