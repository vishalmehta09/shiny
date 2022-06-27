
from cmath import e
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
import itertools

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


@login_required(login_url="/login/")
def generate_bar_chart(request):
      
    if request.method == 'GET':


        if not request.user.is_superuser:
            obj = Graphs.objects.filter(user=request.user)
        elif request.method == "GET" and request.user.is_superuser and request.GET.get('user_id'):
            obj = Graphs.objects.filter(user=int(request.GET.get('user_id')))
            # print(obj)
        else:
            obj = Graphs.objects.filter(user=int(7))

        if obj.exists():
            obj = obj.last()

        
            file_path = obj.upload.path
            data = read_data(file_path)


            context_di = {}
            staff = {}
            
            for i in data['Staff']:
                context_di[i] =  data[data['Staff'] == i]


                staff[i] = dict(Counter(context_di[i]['Role']))
    
            # print(staff,"normal")



            a = data['Staff']
            get_staff = list(a.unique())

            b = data['Sub-Specialty']
            get_sub_specialty = list(b.unique())

            c = data['Location']
            get_location = list(c.unique())

            d = data['Role']
            get_role_data = list(d.unique())
    

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
          
            # names = list(df.Name)

            # primary_surgeon = list(df['Primary Surgeon'])
           
            # first_assist = list(df['First Assist'])
    
            # secondary_assist = list(df['Secondary Assist'])

    
            # user_data = []

            # for i in range(len(names)):
            #     user_data.append({
            #         'Name': names[i],
            #         'Primary Surgeon': primary_surgeon[i], 
            #         'First Assist': first_assist[i], 
            #         'Secondary Assist': secondary_assist[i],

            #         })

            # print(user_data)
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
            name_set = []
            for i in range(len(staff)):
                name_set.append(list(staff.keys())[i])
         

            only_final_data = []

            for d in staff:
                final_data = {
                    "name": d,
                    "Primary Surgeon": staff[d].get('Primary Surgeon', 0),
                    "First Assist": staff[d].get('First Assist', 0),
                    "Secondary Assist": staff[d].get('Secondary Assist', 0),
                }
            
                only_final_data.append(final_data)

            p_list = []
            f_list = []
            s_list = []
            for d in only_final_data:
                p_list.append(d['Primary Surgeon']) 
                f_list.append(d['First Assist']) 
                s_list.append(d['Secondary Assist']) 
                # s_list.append(d['Secondary Assist']) 

            
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
            dashboard3 = (dict(sorted(dashboard13.items(), key=lambda x:x[1], reverse=True)))
           

            keys1 = list((dashboard3.keys()))
            values1 = list((dashboard3.values()))
            
            site = []
            for i in data['Location']:
                site.append(i)
            
            dashboard16 = dict(Counter(site))
            dashboard6 = (dict(sorted(dashboard16.items(), key=lambda x:x[1],reverse=True)))

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
                    "borderColor": ["#ffffff00"],
                    "backgroundColor": color_line_chart(key),
                    })
        
            final_final_data = {
                "datasets": final_data,
                "labels": labels,
            }

            context = { 'keys':keys , 'values':values,
            'keys1': keys1, 'values1': values1 ,
             'keys2': keys2, 'values2': values2, 
             'final_data': final_final_data,
              'labels': labels, 'dashboard23':dashboard23,
               "total_cases":total_cases, "count_of_current_year":count_of_current_year,
                "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 
                'count_of_this_month':count_of_this_month,"final_data_list":datasets,"names":name_set,
                 "get_staff":get_staff,"get_role_data":get_role_data,
                  "get_sub_specialty":get_sub_specialty, "get_location":get_location, 
                  "users":NewUser.objects.all().exclude(is_superuser=True)}

            return render(request, 'home/sample.html', context)
        else:

            return render(request, 'home/sample.html',{'users':NewUser.objects.all().exclude(is_superuser=True)})
    
    if request.method == 'POST':
      
        if not request.FILES.get('document'):
            obj = Graphs.objects.filter(user=request.user)
            if obj.exists():
                obj = obj.last()
            
                upload_file = obj.upload.path           
        else:
            upload_file = request.FILES['document']

        data = read_data(upload_file)

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



        a = data['Staff']
        get_staff = list(a.unique())

        b = data['Sub-Specialty']
        get_sub_specialty = list(b.unique())

        c = data['Location']
        get_location = list(c.unique())

        d = data['Role']
        get_role_data = list(d.unique())
        if request.POST.getlist("Staff"):
            get_data_staff = request.POST.getlist("Staff")
            get_g_staff = data[data["Staff"].isin(get_data_staff)]
        if request.POST.getlist("Role"):
            get_data_role = request.POST.getlist("Role")
            get_g_role = data[data["Role"].isin(get_data_role)]
        if request.POST.getlist("Location") :
            get_data_location = request.POST.getlist("Location")
            get_g_location = data[data["Location"].isin(get_data_location)]
        if request.POST.getlist("Sub-Specialty"):
            get_data_specialty = request.POST.getlist("Sub-Specialty")
            get_g_specialty = data[data["Sub-Specialty"].isin(get_data_specialty)]
            print(get_g_specialty,"get_g")


        context_di = {}

        staff = {}

        for i in data['Staff']:

            context_di[i] = data[data['Staff'] == i]

            staff[i] = dict(Counter(context_di[i]['Role']))


        if set(['Role','Sub-Specialty', 'Location','Date']).issubset(data.columns):
    
            save_obj = Graphs(user=request.user, upload=upload_file)
            save_obj.save()
            if not request.POST.getlist("Staff"):
                name_set = []
                for i in range(len(staff)):
                    name_set.append(list(staff.keys())[i])
                # names = list(df.Name)
                # print(names,"names")
      
            else:
                
                names = get_data_staff
               
            # context_di = {}

            # staff = {}

            # for i in data['Staff']:

            #     context_di[i] = data[data['Staff'] == i]

            #     staff[i] = dict(Counter(context_di[i]['Role']))



          
            name_set = []
            for i in range(len(staff)):
                name_set.append(list(staff.keys())[i])

            only_final_data = []

            for d in staff:
                final_data = {
                    "name": d,
                    "Primary Surgeon": staff[d].get('Primary Surgeon', 0),
                    "First Assist": staff[d].get('First Assist', 0),
                    "Secondary Assist": staff[d].get('Secondary Assist', 0),
                }
            
                only_final_data.append(final_data)

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
            for d in only_final_data:
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
            role = []
            specialty_chart = []
            site =[]
            if request.POST.getlist("Role"):
    
                for i in get_g_role['Role']:
                    role.append(i)
                
                dashboard1 = dict(Counter(role))
                keys = list(dashboard1.keys())
                values = list(dashboard1.values())

                for i in get_g_role['Sub-Specialty']:
                    specialty_chart.append(i)
                
                dashboard13 = dict(Counter(specialty_chart))
                dashboard3 = (dict(sorted(dashboard13.items(), key=lambda x:x[1],reverse=True )))

                keys1 = list(dashboard3.keys())
                values1 = list(dashboard3.values())

                for i in get_g_role['Location']:
                    site.append(i)
                
                dashboard6 = dict(Counter(site))

                keys2 = list(dashboard6.keys())
                values2 = list(dashboard6.values())
                

                
                context_dict = {}
                roles = {}
                for i in get_g_role['Date'].dt.year:
                    context_dict[i] =  get_g_role[get_g_role['Date'].dt.year == i]
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
                        "borderColor": ["#ffffff00"],
                        "backgroundColor": color_line_chart(key),
                        })
            
                final_final_data = {
                    "datasets": final_data,
                    "labels": labels,
                }

                coded_case = []
                for i in get_g_role['Coded Case']:
                    coded_case.append(i)
            
                dashboard23 = dict(Counter(coded_case))

                total_cases = len(get_g_role)
                current_year = date.today().year
                get_date = get_g_role[get_g_role['Date'].dt.year == current_year] 

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
                this_year_month = get_g_role[get_g_role['Date'].dt.to_period('M') == last_months]
                get_g = this_year_month['Role'] == 'Primary Surgeon'
                count_of_last_month = 0
                for i in get_g:
                    if i == True:
                        count_of_last_month+=1
                    else:
                        pass


                today = date.today()
                datem = today.strftime("%Y-%m")
        
                this_year_this_month = get_g_role[get_g_role['Date'].dt.to_period('M') == datem]
                get_role = this_year_this_month['Role'] == 'Primary Surgeon'
                count_of_this_month = 0
                for i in get_role:
                    if i == True:
                        count_of_this_month+=1
                    else:
                        pass

                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":name_set, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty, "get_location":get_location, "dashboard23":dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
                return render(request, 'home/sample.html', context)
                
            else:
                for i in data['Role']:
                    role.append(i)
                
                dashboard1 = dict(Counter(role))
                keys = list(dashboard1.keys())
                values = list(dashboard1.values())
            

            coded_case = []
            for i in data['Coded Case']:
                coded_case.append(i)
        
            dashboard23 = dict(Counter(coded_case))
            specialty_chart = []
            if request.POST.getlist("Sub-Specialty"):
                for i in get_g_specialty['Sub-Specialty']:
                    specialty_chart.append(i)
                
                dashboard3 = dict(Counter(specialty_chart))
                

                keys1 = list(dashboard3.keys())
                values1 = list(dashboard3.values())

                for i in get_g_specialty['Location']:
                    site.append(i)
                
                dashboard6 = dict(Counter(site))

                keys2 = list(dashboard6.keys())
                values2 = list(dashboard6.values())

                for i in get_g_specialty['Role']:
                    role.append(i)
                
                dashboard1 = dict(Counter(role))
                keys = list(dashboard1.keys())
                values = list(dashboard1.values())
                

                
                context_dict = {}
                roles = {}
                for i in get_g_specialty['Date'].dt.year:
                    context_dict[i] =  get_g_specialty[get_g_specialty['Date'].dt.year == i]
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
                        "borderColor": ["#ffffff00"],
                        "backgroundColor": color_line_chart(key),
                        })
            
                final_final_data = {
                    "datasets": final_data,
                    "labels": labels,
                }

                coded_case = []
                for i in get_g_specialty['Coded Case']:
                    coded_case.append(i)

                total_cases = len(get_g_specialty)
                current_year = date.today().year
                get_date = get_g_specialty[get_g_specialty['Date'].dt.year == current_year] 

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
                this_year_month = get_g_specialty[get_g_specialty['Date'].dt.to_period('M') == last_months]
                get_g = this_year_month['Role'] == 'Primary Surgeon'
                count_of_last_month = 0
                for i in get_g:
                    if i == True:
                        count_of_last_month+=1
                    else:
                        pass


                today = date.today()
                datem = today.strftime("%Y-%m")
              
                this_year_this_month = get_g_specialty[get_g_specialty['Date'].dt.to_period('M') == datem]
                get_role = this_year_this_month['Role'] == 'Primary Surgeon'
                count_of_this_month = 0
                for i in get_role:
                    if i == True:
                        count_of_this_month+=1
                    else:
                        pass


                dashboard23 = dict(Counter(coded_case))
                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":name_set, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty, "get_location":get_location, "dashboard23":dashboard23,"total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
                return render(request, 'home/sample.html', context)
                

                
            else:
                for i in data['Sub-Specialty']:
                    specialty_chart.append(i)
                
                dashboard13 = dict(Counter(specialty_chart))
                dashboard3 = (dict(sorted(dashboard13.items(), key=lambda x:x[1], reverse=True)))
                

                keys1 = list(dashboard3.keys())
                values1 = list(dashboard3.values())
                

            site = []
            if request.POST.getlist("Location"):
                for i in get_g_location['Location']:
                    site.append(i)
                
                dashboard6 = dict(Counter(site))

                keys2 = list(dashboard6.keys())
                values2 = list(dashboard6.values())

                for i in get_g_location['Role']:
                    role.append(i)
                
                dashboard1 = dict(Counter(role))
                keys = list(dashboard1.keys())
                values = list(dashboard1.values())
                
                for i in get_g_location['Sub-Specialty']:
                    specialty_chart.append(i)
                
                dashboard3 = dict(Counter(specialty_chart))
                

                keys1 = list(dashboard3.keys())
                values1 = list(dashboard3.values())

                
                context_dict = {}
                roles = {}
                for i in get_g_location['Date'].dt.year:
                    context_dict[i] =  get_g_location[get_g_location['Date'].dt.year == i]
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
                        "borderColor": ["#ffffff00"],
                        "backgroundColor": color_line_chart(key),
                        })
            
                final_final_data = {
                    "datasets": final_data,
                    "labels": labels,
                }

                coded_case = []
                for i in get_g_location['Coded Case']:
                    coded_case.append(i)
            
                dashboard23 = dict(Counter(coded_case))

                total_cases = len(get_g_location)
                current_year = date.today().year
                get_date = get_g_location[get_g_location['Date'].dt.year == current_year] 

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
                this_year_month = get_g_location[get_g_location['Date'].dt.to_period('M') == last_months]
                get_g = this_year_month['Role'] == 'Primary Surgeon'
                count_of_last_month = 0
                for i in get_g:
                    if i == True:
                        count_of_last_month+=1
                    else:
                        pass


                today = date.today()
                datem = today.strftime("%Y-%m")
          
                this_year_this_month = get_g_location[get_g_location['Date'].dt.to_period('M') == datem]
                get_role = this_year_this_month['Role'] == 'Primary Surgeon'
                count_of_this_month = 0
                for i in get_role:
                    if i == True:
                        count_of_this_month+=1
                    else:
                        pass
                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":name_set, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty, "get_location":get_location, "dashboard23":dashboard23,"total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
                return render(request, 'home/sample.html', context)
                
            else:
                for i in data['Location']:
                    site.append(i)
                
                dashboard16 = dict(Counter(site))
                dashboard6 = (dict(sorted(dashboard16.items(), key=lambda x:x[1],reverse=True)))

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
                    "borderColor": ["#ffffff00"],
                    "backgroundColor": color_line_chart(key),
                    })
          
            final_final_data = {
                "datasets": final_data,
                "labels": labels,
            }



            
            
            context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":name_set, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty, "get_location":get_location, "dashboard23":dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
            if request.FILES.get('document'):
                messages.success(request, "File uploaded successfully")
                return render(request, 'home/sample.html', context)
            else:
                return render(request, 'home/sample.html', context)
            

        else:
            messages.error(request, "Invalid header in file")

            return render(request, 'home/sample.html')
    else:
        return render(request, 'home/sample.html')

    
    
   
   
