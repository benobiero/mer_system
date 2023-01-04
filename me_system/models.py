from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import date

THEMATIC=(
    ('SRHR','SRHR'),
    ('H&G','H&G'),
    ('HIV/TB','HIV/TB'),
    ('WLPR','WLPR'),
    ('SILU','SILU')
)

# Create your models here.
class Thematic(models.Model):
    name=models.CharField('Thematic Area', choices=THEMATIC,max_length=200)

    def __str__(self):
        return self.name
class Grant(models.Model):
        
    FREQUENCY=(
        ('Annual','Annual'),
        ('Bi-annual','Bi-annual'),    
    )
    CURRENCY=(
        ('USD','USD'),
        ('Ksh','Ksh'),   
    )

    #thematic_area=MultiSelectField(choices=THEMATIC_CHOIECES)
    name=models.CharField('Enter name',max_length=200)
    thematic_area=models.CharField('enter thematic',max_length=200)
    donor=models.CharField('Donor',max_length=200,blank=True,null=True)
    project_name=models.CharField('Project Name',max_length=200)
    info=models.TextField(blank=True,null=True)
    # person_responsible=MultiSelectField(PERSON_RESPONSIBLE,max_choices=3,max_length=10)
    person_responsible=models.CharField('Person responsible',max_length=100)

    # frequency=MultiSelectField(choices=FREQUENCY,max_choices=2,max_length=10)
    frequency=models.CharField('Enter Frequency',max_length=100)
    project_start=models.DateField(default=now)
    project_end=models.DateField(default=now)
    value=models.IntegerField(blank=True,null=True)
    currency=models.CharField('Choose Currency',max_length=100,default='KSh')
    

    def __str__(self):
        return self.project_name

    

    @property
    def status(self,*args,**kwargs):
        super().save(*args, **kwargs)
        today = date.today()
        time_now = today.strftime("%Y%m%d")
        month=today.strftime("%Y%m")
        if (self.project_end!=None):
            if (self.project_start!=None):
                if (time_now <= self.project_end.strftime("%Y%m%d")) and (time_now>=self.project_start.strftime("%Y%m%d")):
                    status='active'

                    if month==self.project_end.strftime("%Y%m"):
                        status='Ending this month'
                    else:
                        status='active'
                elif time_now>self.project_end.strftime("%Y%m%d"):
                    status='completed'  
                else:
                    status='error'
            
                return status

    
class Name(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):

        return str(self.name)

class Frequency(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):

        return self.name

class Test(models.Model):
    name=models.CharField('your name',max_length=200)
    age=models.CharField('your age',max_length=200)
    other=models.CharField('other details',max_length=200)

    def __str__(self):

        return self.name

class MonthlyTable(models.Model):

    name=models.CharField('thematic name',max_length=200)
    month=models.DateField('Date',default=now)
    intro=models.TextField('introduction',max_length=200)
    project1=models.CharField('project1',max_length=200)
    project2=models.CharField('project2',max_length=200)
    num_accomplished=models.IntegerField('number of accomplished')
    activity_list=models.CharField('activit list',max_length=200)
    num_not_accomplished=models.IntegerField('unaccomplished number')
    unaccomplished_list=models.CharField('unacomplished list',max_length=200)
    num_reason=models.IntegerField('number of reasons')
    reason_list=models.CharField('reason list',max_length=200)
    num_planned=models.IntegerField('number of planned activities',default='0')
    planned_list=models.CharField('planned list',max_length=200,default='activityx')
    lesson=models.TextField('lesson learned',max_length=200)
    challenges=models.TextField('Challenges',max_length=200)
    share=models.CharField('share by',max_length=200)

    def __str__(self):
        return self.activity_list + ' '+ self.name


class Comment(models.Model):
    date=models.DateField('Date',default=now)
    post=models.ForeignKey(MonthlyTable,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField('your name',max_length=200)
    body=models.TextField()
    
    def __str__(self):
        return self.name + " " + self.body

