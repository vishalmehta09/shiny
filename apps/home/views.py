
from urllib.parse import uses_params
from apps.authentication.models import *
from typing import Counter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from .models import Graphs
import pandas as pd
import os
import random
from django.contrib import messages
from datetime import date
from datetime import timedelta


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def read_data(file_path):
        pandas_data = pd.read_excel(file_path, sheet_name='RAW', header=2, parse_dates=True)
        pandas_data_frame= pandas_data.sort_values(by='Date')
        data_frame = pd.DataFrame(pandas_data_frame)
        return data_frame   


def random_color():
    color = '#%06x' % random.randint(0, 0xFFFFFF)
    return color

def color_line_chart(key):
    if key == "Primary Surgeon":
        color = '#398AB9'
    elif key == "First Assist":
        color = '#D8D2CB'
    elif key == "Secondary Assist":
        color = '#1A374D'

    return color

def filter_data(request,df):
    
    get_name = request.GET.get('value')
    role = []
    for i in df[get_name].unique():
        role.append(i)
    
    return role



@login_required(login_url="/login/")
def generate_bar_chart(request):

    if  request.user.is_superuser:

        
        user = NewUser.objects.all().exclude(is_superuser=True)
        id = request.GET.get('id')
        is_admin = request.GET.get('is_admin',None)
        try:
            user_obj = Graphs.objects.filter(user_id=id).last()
            if user_obj is None:
                messages.error(request, 'No data found for this user')
            file_path = user_obj.upload.path
            data = read_data(file_path)
            df1 = pd.read_excel(file_path, sheet_name='Calculations', header=1, parse_dates=True)
            df = df1.sort_values('Total')

            names = list(df.Name)

            primary_surgeon = list(df['Primary Surgeon'])
           
            first_assist = list(df['First Assist'])
    
            secondary_assist = list(df['Secondary Assist'])

    
            user_data = []

            for i in range(len(names)):
                user_data.append({
                    'Name': names[i],
                    'Primary Surgeon': primary_surgeon[i], 
                    'First Assist': first_assist[i], 
                    'Secondary Assist': secondary_assist[i],

                    })

         
            datasets = [
                {
                "label": 'Primary Surgeon',
                "backgroundColor": '#398AB9',
                "data": []
                },
                {
                "label": 'First Assist',
                "backgroundColor": '#D8D2CB',
                "data": []
                },
                {
                "label": 'Secondary Assist',
                "backgroundColor": '#1A374D',
                "data": []
                }
            ]

            p_list = []
            f_list = []
            s_list = []
            for d in user_data:
                p_list.append(d['Primary Surgeon'])
                f_list.append(d['First Assist'])
                s_list.append(d['Secondary Assist'])


            for dataset in datasets:
                if dataset['label'] == 'Primary Surgeon':
                    dataset['data'] = p_list
                elif dataset['label'] == 'First Assist':
                    dataset['data'] = f_list
                elif dataset['label'] == 'Secondary Assist':
                    dataset['data'] = s_list



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
                return JsonResponse({'keys': keys, 'values': values, 'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2,"final_data_list":datasets,"names":names,})
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
      
            df1 = pd.read_excel(file_path, sheet_name='Calculations', header=1, parse_dates=True)
            df = df1.sort_values('Total')

           
            if request.GET.get('value') is not None:
                get_val = filter_data(request,data)
                print(get_val)
 
            total_cases = len(data)
            current_year = date.today().year
            get_date = data[data['Date'].dt.year == current_year] 

            date_gt = get_date['Date'].dt.to_period('M') > '2022-06'
            count_of_current_year = 0
            for u in list(date_gt):
                if u == True:
                    count_of_current_year+=1
                else:
                    pass
            this_year_ps = get_date['Role'] == 'Primary Surgeon'
    
            count_of_current = 0
            for i in this_year_ps:
                if i == True:
                    count_of_current+=1
                else:
                    pass
            today = date.today()
            first = today.replace(day=1)
            lastMonth = first - timedelta(days=1)
            last_months = lastMonth.strftime("%Y-%m")
            this_year_month = data[data['Date'].dt.to_period('M') == last_months]
            get_g = this_year_month['Role'] == 'Primary Surgeon'
            count_of_last_month = 0
            for i in get_g:
                if i == True:
                    count_of_last_month+=1
                else:
                    pass


            today = date.today()
            datem = today.strftime("%Y-%m")
        
            this_year_this_month = data[data['Date'].dt.to_period('M') == datem]
            get_role = this_year_this_month['Role'] == 'Primary Surgeon'
            count_of_this_month = 0
            for i in get_role:
                if i == True:
                    count_of_this_month+=1
                else:
                    pass

            coded_case = []
            for i in data['Coded Case']:

                coded_case.append(i)

            
            dashboard23 = (dict(Counter(coded_case)))
          
            names = list(df.Name)

            primary_surgeon = list(df['Primary Surgeon'])
           
            first_assist = list(df['First Assist'])
    
            secondary_assist = list(df['Secondary Assist'])

    
            user_data = []

            for i in range(len(names)):
                user_data.append({
                    'Name': names[i],
                    'Primary Surgeon': primary_surgeon[i], 
                    'First Assist': first_assist[i], 
                    'Secondary Assist': secondary_assist[i],

                    })

         
            datasets = [
                {
                "label": 'Primary Surgeon',
                "backgroundColor": '#398AB9',
                "data": []
                },
                {
                "label": 'First Assist',
                "backgroundColor": '#D8D2CB',
                "data": []
                },
                {
                "label": 'Secondary Assist',
                "backgroundColor": '#1A374D',
                "data": []
                }
            ]

            p_list = []
            f_list = []
            s_list = []
            for d in user_data:
                p_list.append(d['Primary Surgeon'])
                f_list.append(d['First Assist'])
                s_list.append(d['Secondary Assist'])


            for dataset in datasets:
                if dataset['label'] == 'Primary Surgeon':
                    dataset['data'] = p_list
                elif dataset['label'] == 'First Assist':
                    dataset['data'] = f_list
                elif dataset['label'] == 'Secondary Assist':
                    dataset['data'] = s_list

            role = []
            for i in data['Role']:
                role.append(i)
            
            dashboard1 = dict(Counter(role))
            keys = list(dashboard1.keys())
            values = list(dashboard1.values())


            specialty_chart = []
            for i in data['Sub-Specialty']:
                specialty_chart.append(i)
            
            dashboard13 = dict(Counter(specialty_chart))
            dashboard3 = (dict(sorted(dashboard13.items(), key=lambda x:x[1], )))
           

            keys1 = list((dashboard3.keys()))
            values1 = list((dashboard3.values()))
            
            site = []
            for i in data['Location']:
                site.append(i)
            
            dashboard16 = dict(Counter(site))
            dashboard6 = (dict(sorted(dashboard16.items(), key=lambda x:x[1],)))

            keys2 = list(dashboard6.keys())
            values2 = list(dashboard6.values())

            context_dict = {}
            roles = {}
            df = data['Date'].dt.year
        
            for i in data['Date'].dt.year:
                context_dict[i] =  data[data['Date'].dt.year == i]
                roles[i] = dict(Counter(context_dict[i]['Role']))
            
    
            labels = []
            role_keys = []
            raw_data = []
            for role in roles:

                labels.append(role)
                role_key = list(roles[role].keys())
                role_keys.append(role_key)
                raw_data.append(roles[role])   
            final_data = []
            for key in role_keys[1]:
                data = []
                for raw in raw_data:
                    data.append(raw.get(key,0))
           
                final_data.append({
                    "label": key,
                    "data": data,
                    "borderColor": color_line_chart(key),
                    "backgroundColor": color_line_chart(key),
                    })
        
            final_final_data = {
                "datasets": final_data,
                "labels": labels,
            }

            context = { 
            'keys':keys , 'values':values,
            'keys1': keys1, 'values1': values1 ,
             'keys2': keys2, 'values2': values2, 
             'final_data': final_final_data, 
             'labels': labels, 'dashboard23':dashboard23, 
             "total_cases":total_cases,
              "count_of_current_year":count_of_current_year,
               "count_of_current":count_of_current,
               "final_data_list":datasets,"names":names,
                "count_of_last_month":count_of_last_month, 
                'count_of_this_month':count_of_this_month,
                }

            return render(request, 'home/sample.html', context)
        else:
            return render(request, 'home/sample.html')
        

    if request.method == 'POST':
    
        upload_file = request.FILES['document']

        file_extension = os.path.splitext(upload_file.name)[1]

        valid_extensions = [ ".csv", ".CSV", ".xlsx", ".XLSX", ".xls", ".XLS"]
        if not file_extension.lower() in valid_extensions:
            msg = "Invalid file, select a valid CSV file"

            messages.error(request, msg)

            return redirect('generate_bar_chart')
       
        df1 = pd.read_excel(upload_file, sheet_name='Calculations', header=1, parse_dates=True)
        df = df1.sort_values('Total')

        data = read_data(upload_file)
        # print(data)
        # r_le = []
        # val_e = []
        # for j in data["Role"]:
        #     r_le.append(j)
        # for i in data["Staff"]:
        #     if i in r_le[""]:
        #         val_e.append(i)
                
                    
        # print(val_e)

        if set(['Role','Sub-Specialty', 'Location','Date']).issubset(data.columns):
        
            
            save_obj = Graphs(user=request.user, upload=upload_file)
            save_obj.save()
    
            
            names = list(df.Name)
            primary_surgeon = list(df['Primary Surgeon'])
            first_assist = list(df['First Assist'])
            secondary_assist = list(df['Secondary Assist'])

            user_data = []


            for i in range(len(names)):
                user_data.append({
                   
                    'Primary Surgeon': primary_surgeon[i], 
                    'First Assist': first_assist[i], 
                    'Secondary Assist': secondary_assist[i]
                    })
            # print(user_data)
            # context_di = {}

            # staff = {}

            # for i in data['Staff']:

            #     context_di[i] = data[data['Staff'] == i]

            #     staff[i] = dict(Counter(context_di.get(i,0)['Role']))



            # get_starr = list(staff.values())
            # print(get_starr)

            # user_data = [{'Secondary Assist': 8, 'First Assist': 2, 'Primary Surgeon': 3}, {'First Assist': 3}, {'Secondary Assist': 10, 'First Assist': 6, 'Primary Surgeon': 1}, {'Secondary Assist': 2, 'First Assist': 3}, {'Secondary Assist': 1}, {'Secondary Assist': 36, 'First Assist': 14, 'Primary Surgeon': 3}, {'First Assist': 3, 'Secondary Assist': 2, 'Primary Surgeon': 1}, {'Secondary Assist': 4, 'Primary Surgeon': 1, 'First Assist': 3}, {'Secondary Assist': 13, 'Primary Surgeon': 28, 'First Assist': 29}, {'Secondary Assist': 18, 'Primary Surgeon': 7, 'First Assist': 5}, {'First Assist': 6, 'Primary Surgeon': 4}, {'First Assist': 1, 'Secondary Assist': 1}, {'First Assist': 1, 'Secondary Assist': 2}, {'First Assist': 3, 'Primary Surgeon': 1}, {'Secondary Assist': 3, 'Primary Surgeon': 11, 'First Assist': 3}, {'First Assist': 7, 'Primary Surgeon': 2}, {'Primary Surgeon': 5, 'Secondary Assist': 11, 'First Assist': 3}, {'Secondary Assist': 28, 'First Assist': 3, 'Primary Surgeon': 1}, {'First Assist': 3, 'Primary Surgeon': 1}, {'Primary Surgeon': 3}, {'First Assist': 3, 'Secondary Assist': 2}]

            datasets = [
                {
                "label": 'Primary Surgeon',
                "backgroundColor": '#398AB9',
                "data": []
                },
                {
                "label": 'First Assist',
                "backgroundColor": '#D8D2CB',
                "data": []
                },
                {
                "label": 'Secondary Assist',
                "backgroundColor": '#1A374D',
                "data": []
                }
            ]

            p_list = []
            f_list = []
            s_list = []
            for d in user_data:
                print(d)
                s_list.append(d['Secondary Assist'])
                f_list.append(d['First Assist'])
                p_list.append(d['Primary Surgeon'])
               
               


            for dataset in datasets:
                if dataset['label'] == 'Primary Surgeon':
                    dataset['data'] = p_list
                elif dataset['label'] == 'First Assist':
                    dataset['data'] = f_list
                elif dataset['label'] == 'Secondary Assist':
                    dataset['data'] = s_list
            
            coded_case = []
            for i in data['Coded Case']:
                coded_case.append(i)

   
            dashboard23 = (dict(Counter(coded_case)))

            
            role = []
            for i in data['Role']:
                role.append(i)
            
            dashboard1 = dict(Counter(role))
            keys = list(dashboard1.keys())
            values = list(dashboard1.values())



            specialty_chart = []

            for i in data['Sub-Specialty']:
                specialty_chart.append(i)
            
            dashboard13 = dict(Counter(specialty_chart))
            dashboard3 = (dict(sorted(dashboard13.items(), key=lambda x:x[1]), ))
            

            keys1 = list(dashboard3.keys()) 
            values1 = list(dashboard3.values())


            site = []
            for i in data['Location']:
                site.append(i)
            
            dashboard16 = dict(Counter(site))
            dashboard6 = (dict(sorted(dashboard16.items(), key=lambda x:x[1])))

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
                role_key = list(roles[role].keys())
                role_keys.append(role_key)
                raw_data.append(roles[role])

            final_data = []
            for key in role_keys[1]:
                data = []
                for raw in raw_data:
        
                    data.append(raw.get(key,0))
               

                final_data.append({
                    "label": key,
                    "data": data,
                    "borderColor": color_line_chart(key),
                    "backgroundColor": color_line_chart(key),
                    })
          
            final_final_data = {
                "datasets": final_data,
                "labels": labels,
            }

            
            
            context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":names,"dashboard23":dashboard23}
            messages.success(request, "File uploaded successfully")
            return render(request, 'home/sample.html', context)
        else:
            messages.error(request, "Invalid header in file")

            return render(request, 'home/sample.html')
    else:
        return render(request, 'home/sample.html')

    
    
   
   
