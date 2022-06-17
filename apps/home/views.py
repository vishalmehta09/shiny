
from traceback import print_tb
from unittest import result
from urllib.parse import uses_params
from django.contrib.auth.models import User
from typing import Counter
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from numpy import empty
from .models import Graphs
import pandas as pd
import os
import random
from django.contrib import messages
from datetime import date

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def read_data(file_path):
        pandas_data_frame = pd.read_excel(file_path, sheet_name='RAW', header=2, parse_dates=True)
        data_frame = pd.DataFrame(pandas_data_frame)
        return data_frame   


def random_color():
    
    color = '#%06x' % random.randint(0, 0xFFFFFF)
    return color


@login_required(login_url="/login/")
def generate_bar_chart(request):

    if  request.user.is_superuser:

        
        user = User.objects.all().exclude(is_superuser=True)
        id = request.GET.get('id')
        is_admin = request.GET.get('is_admin',None)
        try:
            user_obj = Graphs.objects.filter(user_id=id).last()
            if user_obj is None:
                messages.error(request, 'No data found for this user')
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
            
            # return render(request, 'home/sample.html')
        
        
        return render(request, 'home/new_sample.html', {'users': user,})
    
  
    if request.method == 'GET':

        obj = Graphs.objects.filter(user=request.user)
        if obj.exists():
            obj = obj.last()
        
            file_path = obj.upload.path
            data = read_data(file_path)
            total_cases = len(data)
            current_year = date.today().year
            # abv = data['Date'].dt.month
            # print(abv, "abvvvvvvvvv")
            get_date = data[data['Date'].dt.year == current_year] 
            aaaa = get_date['Date'].dt.to_period('M') == '2022-03'
            print(aaaa, "sss")
            if aaaa is not True:
                abc = 0
            else:
                abc = len(aaaa)
            print(abc, "hghghg")
            # print(aaaa, "aaaaaaaaaaaa")
            # df['StartDate'].dt.to_period('M')
            m_d = data['Date'].dt.to_period('M')
            # print(data['Date'].dt.to_period('M'), "month")
            
            y = current_year
            s = '-07' 

            limit = '2022-07'
            # print(limit, "limit")
            # print(data['Date'].dt.month, "data['Date'].dt.monthdata['Date'].dt.month")
            abc = len(data[data['Date'].dt.to_period('M') >= limit] )
            # abc = len(data[data['Date'] >= limit])
            # print("abc", abc)
            # data[data['Date'].dt.month >= 7]
            # print(get_date, "get_dateget_date")
            coded_case = []
            for i in data['Coded Case']:
                coded_case.append(i)
        
            dashboard23 = dict(Counter(coded_case))
            # print(dashboard23, "coded_casecoded_casecoded_casecoded_case")
            # print(data)
            role = []
            for i in data['Role']:
                role.append(i)
        
            dashboard2 = dict(Counter(role))
    
            keys = list(dashboard2.keys())
            # print(keys)
            values = list(dashboard2.values())
            # print(values)

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

            context_dict = {}
            roles = {}
            df = data['Date'].dt.year
            # print(df, "dfffff")
            for i in data['Date'].dt.year:
                context_dict[i] =  data[data['Date'].dt.year == i]
                roles[i] = dict(Counter(context_dict[i]['Role']))
            
            # print(roles)
            labels = []
            role_keys = []
            raw_data = []
            for role in roles:
                # print(role, "roleeeeee")
                labels.append(role)
                role_keys = list(roles[role].keys())
                raw_data.append(roles[role])
                
            final_data = []
            for key in role_keys:
                data = []
                for raw in raw_data:
                    data.append(raw.get(key,0))
                
                final_data.append({
                    "label": key,
                    "data": data,
                    "borderColor": random_color(),
                    "backgroundColor": random_color(),
                    "fill": "true",
                    })
            # print(labels.sort(), "labelslabelslabels")
            # label = labels.sort()
            # print(label, "label")
            final_final_data = {
                "datasets": final_data,
                "labels": labels,
            }

            context = { 'keys': keys, 'values': values, 'keys1': keys1, 'values1': values1 , 'keys2': keys2, 'values2': values2, 'final_data': final_final_data, 'labels': labels, 'dashboard23':dashboard23, "total_cases":total_cases}
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


            context_dict = {}
            roles = {}
            for i in data['Date'].dt.year:
                context_dict[i] =  data[data['Date'].dt.year == i]
                roles[i] = dict(Counter(context_dict[i]['Role']))
            
            labels = []
            role_keys = []
            raw_data = []
            for role in roles:
                labels.append(role)
                role_keys = list(roles[role].keys())
                raw_data.append(roles[role])

            final_data = []
            for key in role_keys:
                data = []
                for raw in raw_data:
                    print(raw)
                    data.append(raw.get(key,0))
                print("final res",data)
            
                final_data.append({
                    "label": key,
                    "data": data,
                    "borderColor": random_color(),
                    "backgroundColor": random_color(),
                    "fill": "true",
                    })
          
            final_final_data = {
                "datasets": final_data,
                "labels": labels,
            }
            
            context = { 'keys': keys, 'values': values, 'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels}
            messages.success(request, "File uploaded successfully")
            return render(request, 'home/sample.html', context)
        else:
            messages.error(request, "Invalid header in file")

            return render(request, 'home/sample.html')
    else:
        return render(request, 'home/sample.html')

    
    
   
   
