from django.shortcuts import render,redirect
from . forms import GrantForm,CommentForm
from . models import Grant,Thematic,Name,Frequency,Test,MonthlyTable,Comment
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
import re
from datetime import date
from pandas.tseries.offsets import DateOffset

today = date.today()
time_now = int(today.strftime("%Y%m%d"))
month=today.strftime("%Y%m")
time_yesterday=pd.to_datetime(time_now,format='%Y%m%d')
last_month=time_yesterday.strftime('%Y-%m')
last_month1=pd.to_datetime(time_yesterday,format='%Y%m%d').strftime('%B')
current_month=today.strftime('%B')




def home(request):
    
    return render(request,'home.html',{})

def project_dashboard(request):

    return render(request,'project_page/project_dashboard.html')

def add_project(request):
    thematic = Thematic.objects.all()
    frequency = Frequency.objects.all()
    name = Name.objects.all()
    context = {
        'thematic': thematic,
        'name':name,
        'frequency':frequency,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'project_page/add_project.html', context)

    if request.method == 'POST':
        project_name = request.POST['project_name']

        if not project_name:
            messages.error(request, 'Project name is required is required')
            return render(request, 'project_page/add_project.html', context)
        name = request.POST['name']
        donor = request.POST['donor']
        thematic_area = request.POST['thematic_area']
        project_start= request.POST['project_start']
        project_end= request.POST['project_end']
        info = request.POST['info']
        person_responsible = request.POST['person_responsible']
        frequency = request.POST['frequency']
        value = request.POST['value']
        currency = request.POST['currency']

        if not name:
            messages.error(request, 'description is required')
            return render(request, 'project_page/add_project.html', context)

        

        Grant.objects.create( name=name,project_name=project_name, thematic_area=thematic_area,donor=donor,
                               info=info,person_responsible=person_responsible, project_start=project_start,
                               project_end=project_end,value=value,currency=currency,frequency=frequency)
        messages.success(request, 'Grants saved successfully')

        return redirect('home')

def search_grant(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        grant = Grant.objects.filter(
            project_name__istartswith=search_str) | Grant.objects.filter(
            thematic_area__istartswith=search_str) | Grant.objects.filter(
            info__icontains=search_str) | Grant.objects.filter(
            project_start__icontains=search_str)|Grant.objects.filter(
            project_end__istartswith=search_str) |Grant.objects.filter(
            name__istartswith=search_str)
        data = grant.values()
        return JsonResponse(list(data), safe=False)


def test(request):
    context={}
    


    if request.method == 'GET':
        return render(request, 'project_page/test.html', context)

    if request.method == 'POST':
        activities=[]
        name = request.POST['name']

        other=request.POST['fieldCounter']
     
       
        print(other)
     

        if not name:
            messages.error(request, 'your name is required is required')
            return render(request, 'project_page/test.html', context)
        age = request.POST['age']
        
        if not age:
            messages.error(request, 'description is required')
            return render(request, 'project_page/test.html', context)
    return redirect('test')

    
   
def reporting_tools(request):

    return render(request,'Reports/reporting_tools.html',{})

def monthly_tool(request):

    global context
    
    activity_list=[]
    unaccomplished_list=[]
    reason_list=[]
    planned_list=[]
 

    if request.method == 'POST':

        thematic=request.POST['thematic']
        month=request.POST['month']
        intro=request.POST.get('intro')

        project1=request.POST['project1']
        project2=request.POST.get('project2')

        num_accomplished=request.POST['num_accomplished']

        print(month)
        print(thematic)
        
        if len(num_accomplished)!=0:

            for i in range(0,int(num_accomplished)):
                activity=request.POST['activity' + str(i)]
                activity_list.append(activity)
   

        num_not_accomplished = request.POST['num_not_accomplished']
        if len(num_not_accomplished) !=0:
            for i in range(0,int(num_not_accomplished)):
                unaccomplished=request.POST['uncomplished' + str(i)]
                unaccomplished_list.append(unaccomplished)

        num_reason=request.POST['num_reason']
        if len(num_reason) !=0:
            for i in range(0,int(num_reason)):
                reason=request.POST['reason' + str(i)]
                reason_list.append(reason)

        num_planned = request.POST['num_planned']
        if len(num_planned) !=0:
            for i in range(0,int(num_planned)):
                planned=request.POST['planned' + str(i)]
                planned_list.append(planned)

        lesson=request.POST['lesson']
        challenges=request.POST['challenges']

        share=request.POST['share']

        # validating the form

        

    

        MonthlyTable.objects.create(
            name=thematic,month=month,intro=intro,project1=project1,project2=project2,
            num_accomplished=num_accomplished,activity_list=activity_list,num_not_accomplished=num_not_accomplished,
            unaccomplished_list=unaccomplished_list,num_reason=num_reason,reason_list=reason_list,
            num_planned=num_planned,planned_list=planned_list,challenges=challenges,lesson=lesson,share=share
        )

        return redirect('home')
   
            
      # Display the errors to the user
           
    context={
       
        'activity':activity_list,
       
        'uncomplished':unaccomplished_list,
   
        'reason':reason_list,
   
        'planned':planned_list,
       

    }

   
    
   

    if request.method == 'GET':
        return render(request, 'Reports/monthly_tool.html', context)


def preview_monthly(request):
    monthly_tool(request)

    global context

    return render(request, 'Reports/preview_monthly.html', context)

 # function that cleans  activity reported   
def activity_string(col):
    # initialize an empty string
    col=col.replace('[', ' ').replace(']', ' ').replace("'",' ')

    # return string 
    return col

def dashboard(request):

    
    if request.method=='GET':
        thematic = request.GET.get('thematic','HIV/TB')
        input = request.GET.get('input', last_month)
        print(thematic)
        print(input)

        monthly_report=MonthlyTable.objects.filter(month__icontains=input)
        
        monthly_filter=monthly_report.values('name','month','num_accomplished','activity_list',
    'num_not_accomplished','unaccomplished_list','num_reason','reason_list','num_planned','planned_list','share')

  

        monthly_df=pd.DataFrame(monthly_filter)
        group_df=monthly_df
        group_df.reset_index(inplace=True)

        


        if monthly_df.shape[0]!=0:


            # define new table

            monthly_report=MonthlyTable.objects.filter(month__icontains=input)
            monthly_thematic=MonthlyTable.objects.filter(name__icontains=thematic)
            thematic_df=pd.DataFrame(monthly_thematic.values())
            
       
                    

            # getting the  number of planned,completed and unaccomplished activies

            data_completed=group_df['num_accomplished'].sum()
            data_not_completed=group_df['num_not_accomplished'].sum()
            data_planned=group_df['num_planned'].sum()

            #  creating df for  completed , unaccomplished and planned activities
            completed_df=monthly_df[['name','month','activity_list']].copy()
            unaccomplished_df=monthly_df[['name','month','unaccomplished_list']].copy()
            planned_df=monthly_df[['name','month','planned_list']].copy()
    
            # cleaning columns
            completed_df['activity_list']=completed_df['activity_list'].apply(activity_string)
            unaccomplished_df['unaccomplished_list']=unaccomplished_df ['unaccomplished_list'].apply(activity_string)
            planned_df['planned_list']=planned_df ['planned_list'].apply(activity_string)
    
            # more cleaning, and this time every activity is listed verticaly
            completed_clean = completed_df.assign(activity_list=completed_df.activity_list.str.split(",")).explode('activity_list')
            unaccomplished_clean = unaccomplished_df.assign(unaccomplished_list=unaccomplished_df.unaccomplished_list.str.split(",")).explode('unaccomplished_list')
            planned_clean = planned_df.assign(planned_list=planned_df.planned_list.str.split(",")).explode('planned_list')

  

            # adding month column
    
            completed_clean["Month"] =completed_clean["month"].apply(lambda x: x.strftime('%B'))
            unaccomplished_clean["Month"] =unaccomplished_clean["month"].apply(lambda x: x.strftime('%B'))
            planned_clean['date_plus1'] = planned_clean.month + DateOffset(months=1)
     
            planned_clean["Month"] =planned_clean["month"].apply(lambda x: x.strftime('%B'))
            planned_clean['date_plus1'] =planned_clean['date_plus1'].apply(lambda x: x.strftime('%Y-%B'))
      
            next_month=planned_clean['date_plus1'].unique()
            next_month=next_month[0]
    

    # converting to json
            json_completed=completed_clean.reset_index().to_json(orient='records')
            completed_table=[]
            completed_table=json.loads(json_completed)

            json_unaccomplished=unaccomplished_clean.reset_index().to_json(orient='records')
            unaccomplished_table=[]
            unaccomplished_table=json.loads(json_unaccomplished)

            json_planned=planned_clean.reset_index().to_json(orient='records')
            planned_table=[]
            planned_table=json.loads(json_planned)


    

            context={
        'monthly_report':monthly_report,
        'data_completed':data_completed,
        'data_not_completed':data_not_completed,
        'data_planned':data_planned,
        'completed_table':completed_table,
        'unaccomplished_table':unaccomplished_table,
        'planned_table':planned_table,
        'last_month':last_month1,
        'current_month':current_month,
        'input':input,
        'next_month':next_month
    }

    
  

            return render(request,'dashboard.html',context)
    return render(request,'dashboard.html',{'input':input})
    
    
   
    
class DashbordCharts(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        monthly_report=MonthlyTable.objects.all()
        monthly_filter=monthly_report.values('name','month','num_accomplished','activity_list',
        'num_not_accomplished','unaccomplished_list','num_reason','reason_list','num_planned','planned_list','share')

        monthly_df=pd.DataFrame(monthly_filter)
        group_df=monthly_df
        group_df.reset_index(inplace=True)
        labels=group_df['name']
        data_completed=group_df['num_accomplished']
        data_not_completed=group_df['num_not_accomplished']
        data_planned=group_df['num_planned'].to_list()
        data={
            'labels':labels,
            'data1':data_completed,
            'data2':data_not_completed,
            'data3':data_planned

        }
       

        return Response(data)



def unaccomplished(request):

    monthly_report=MonthlyTable.objects.filter(month__icontains=last_month)
    monthly_filter=monthly_report.values('name','month',
    'unaccomplished_list','reason_list')

    monthly_df=pd.DataFrame(monthly_filter)

    unaccomplished_df=monthly_df[['name','month','unaccomplished_list','reason_list']]

    unaccomplished_df['unaccomplished_list']=unaccomplished_df ['unaccomplished_list'].apply(activity_string)
    unaccomplished_df['reason_list']=unaccomplished_df ['reason_list'].apply(activity_string)
    

    unaccomplished_clean = unaccomplished_df.assign(unaccomplished_list=unaccomplished_df.unaccomplished_list.str.split(",")).explode('unaccomplished_list')
    unaccomplished_clean2 = unaccomplished_df.assign(reason_list=unaccomplished_df.reason_list.str.split(",")).explode('reason_list')
    

    unaccomplished_clean=unaccomplished_clean[['name','month','unaccomplished_list']]
    unaccomplished_clean2=unaccomplished_clean2[['reason_list']]
    final_df= pd.concat([unaccomplished_clean2,unaccomplished_clean], axis=1)


    #define new DataFrame that merges columns with same names togethe 

    final_df["Month"] =final_df["month"].apply(lambda x: x.strftime('%B'))
    

    # converting to json
    json_reason=final_df.reset_index().to_json(orient='records')
    reason_table=[]
    reason_table=json.loads(json_reason)



    context={
      'reason_table':reason_table
    }
    return render(request,'activity/unaccomplished.html',context)

def monthly_report(request):
    report=MonthlyTable.objects.all()

    return render(request,'Reports/under_review.html',{'month':report})

def month_report_detail(request,pk):

    month_report=MonthlyTable.objects.filter(pk=pk)
    month_report2=MonthlyTable.objects.filter(pk=pk)

    monthly_df=pd.DataFrame(month_report.values())

    # cleaning columns
    monthly_df['activity_list']=monthly_df['activity_list'].apply(activity_string)
    monthly_df['unaccomplished_list']=monthly_df['unaccomplished_list'].apply(activity_string)
    monthly_df['planned_list']=monthly_df ['planned_list'].apply(activity_string)
    monthly_df['reason_list']=monthly_df ['reason_list'].apply(activity_string)

    # more cleaning, and this time every activity is listed verticaly
    num_not_accomplished=monthly_df['num_not_accomplished']
    num_accomplished=monthly_df['num_accomplished']
    num_planned=monthly_df['num_planned']
    num_resaon=monthly_df['num_reason']
    completed_clean = monthly_df.assign(activity_list=monthly_df.activity_list.str.split(",")).explode('activity_list')
    unaccomplished_clean = monthly_df.assign(unaccomplished_list=monthly_df.unaccomplished_list.str.split(",")).explode('unaccomplished_list')
    planned_clean = monthly_df.assign(planned_list=monthly_df.planned_list.str.split(",")).explode('planned_list')
    reason_clean = monthly_df.assign(planned_list=monthly_df.reason_list.str.split(",")).explode('reason_list')

    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('under-review')
       
    form=CommentForm()



    return render(request,'Reports/monthly_detail.html',{'month':month_report,'month2':month_report2,'form':form})

def data_entry(request):

    return render(request,'data_entry/entry_tool.html',{})
