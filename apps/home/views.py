
from urllib.parse import uses_params
from django.contrib.auth.models import User
from typing import Counter
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import Graphs
import pandas as pd
import os
from django.contrib import messages


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
        is_admin = request.GET.get('is_admin',None)
        try:
            user_obj = Graphs.objects.filter(user_id=id).last()
            file_path = user_obj.upload.path
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

            if is_admin:
                return JsonResponse({'keys': keys, 'values': values, 'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2})
            return render(request, 'home/sample.html', {'keys': keys, 'values': values})
        except:
            pass
        
        
        return render(request, 'home/new_sample.html', {'users': user,})
    
  
    if request.method == 'GET':

        obj = Graphs.objects.filter(user=request.user)
        if obj.exists():
            obj = obj.last()
        
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

        file_extension = os.path.splitext(upload_file.name)[1]

        valid_extensions = [ ".csv", ".CSV", ".xlsx", ".XLSX", ".xls", ".XLS"]

        if not file_extension.lower() in valid_extensions:
            msg = "Invalid file, select a valid CSV file"
            messages.error(request, msg)
            return render(request,'home/sample.html')

        #read the file and convert to data frame.
        data = read_data(upload_file)
        if set(['Role','Sub-Specialty', 'Location','Date']).issubset(data.columns):
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
            messages.success(request, "File uploaded successfully")
            return render(request, 'home/sample.html', context)
        else:
            messages.error(request, "Invalid header in file")

            return render(request, 'home/sample.html')
    else:
        return render(request, 'home/sample.html')

    
    
   
   
