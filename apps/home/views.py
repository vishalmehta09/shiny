
from urllib.parse import uses_params
from django.contrib.auth.models import User
from typing import Counter

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Graphs
import pandas as pd
import os


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def read_data(file_path):
        pandas_data_frame = pd.read_excel(file_path, sheet_name='RAW', header=2, )
        data_frame = pd.DataFrame(pandas_data_frame)
        return data_frame


@login_required(login_url="/login/")
def generate_bar_chart(request):

    if  request.user.is_superuser:

        user = User.objects.all().exclude(is_superuser=True)
        id = request.GET.get('id')
        # print(User.objects.filter(id=id))
        user = User.objects.filter(id=id)
        pass
    

    

        # graph_obj = Graphs.objects.all()
        # # print(graph_obj.values())

        # get_obj = Graphs.objects.filter(id=id).first()
        # print(get_obj)
        
        return render(request, 'home/admin.html', {'users': user})
  
    elif request.method == 'GET':
        
        obj = Graphs.objects.filter(user=request.user)
        if obj.exists():
            obj = obj.first()
        
            file_path = obj.upload.path
        
            data = read_data(file_path)

            # print(data)
            role = []
            for i in data['Role']:
                role.append(i)
        
            dashboard2 = dict(Counter(role))
    
            keys = list(dashboard2.keys())
            values = list(dashboard2.values())

            specialty_chart = []
            for i in data['Sub-Specialty']:
                specialty_chart.append(i)
            
            dashboard3 = dict(Counter(specialty_chart))

            keys1 = list(dashboard3.keys())
            values1 = list(dashboard3.values())
            
            site = []
            for i in data['Location']:
                site.append(i)
            
            dashboard6 = dict(Counter(site))

            keys2 = list(dashboard6.keys())
            values2 = list(dashboard6.values())

            context = { 'keys': keys, 'values': values, 'keys1': keys1, 'values1': values1 , 'keys2': keys2, 'values2': values2}

            return render(request, 'home/sample.html', context)
        else:
            return render(request, 'home/sample.html')
        

    if request.method == 'POST':
    
        # Get the data from the form
        upload_file = request.FILES['document']
 

        #save uploaded file to the server
        # fs = FileSystemStorage()
        # filename = fs.save(upload_file.name, upload_file)
        # path = os.getcwd() 
        # file_directory = path+"/media/"+filename

        #read the file and convert to data frame.
        data = read_data(upload_file)
        # print(data)
        save_obj = Graphs(user=request.user, upload=upload_file)
        save_obj.save()


        role = []
        for i in data['Role']:
            role.append(i)
    
        dashboard2 = dict(Counter(role))
  
        keys = list(dashboard2.keys())
        values = list(dashboard2.values())


        specialty_chart = []

        for i in data['Sub-Specialty']:
            specialty_chart.append(i)
        
        dashboard3 = dict(Counter(specialty_chart))
        

        keys1 = list(dashboard3.keys())
        values1 = list(dashboard3.values())


        site = []
        for i in data['Location']:
            site.append(i)
        
        dashboard6 = dict(Counter(site))

        keys2 = list(dashboard6.keys())
        values2 = list(dashboard6.values())
        
        context = { 'keys': keys, 'values': values, 'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 }
        
        
        return render(request, 'home/sample.html', context)
    else:
        return render(request, 'home/sample.html')

        
    
   


 

    # _year = []
    # for i in data['Date'].dt.year:

    #     _year.append(i)
    
    # dashboard4 = dict(Counter(_year))
    # # print(dashboard4)

    # _month = []
    # for i in data['Date'].dt.month_name():

    #     _month.append(i)
            
    # dashboard5 = dict(Counter(_month))
    # # print(dashboard5)
    # keys7 = list(dashboard4.keys())
  
    # values7 = list(dashboard5.keys())

    
       
    #  'keys3': keys3, 'values3': values3,  'keys6': keys6, 'values6': values6, 'keys7': keys7, 'values7': values7}
    
    
   
   
