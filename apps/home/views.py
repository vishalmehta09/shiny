

from tkinter import E
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
def color_line_chart(key):

    if key == "Primary Surgeon":
        color = '#398AB9'

    elif key == "First Assist":
        color = '#D8D2CB'
    elif key == "Secondary Assist":
    
        color = '#1A374D'
    return color

def random_color():
    
    color = '#%06x' % random.randint(0, 0xFFFFFF)
    return color


@login_required(login_url="/login/")
def generate_bar_chart(request):

    # if  request.user.is_superuser:
    #     user = User.objects.all().exclude(is_superuser=True)
    #     return render(request, 'home/sample.html',{'user':user})

        
        # user = User.objects.all().exclude(is_superuser=True)
        
        # id = request.GET.get('id')
        # print(id, "id")
        # is_admin = request.GET.get('is_admin',None)
        # try:
        #     user_obj = Graphs.objects.filter(user_id=id).last()
        #     if user_obj is None:
        #         messages.error(request, 'No data found for this user')
        #     file_path = user_obj.upload.path
        #     data = read_data(file_path)

        #     a = data['Staff']
        #     get_staff = list(a.unique())
        #     print(get_staff,"get_staff")
        #     b = data['Sub-Specialty']
        #     get_sub_specialty = list(b.unique())

        #     c = data['Location']
        #     get_location = list(c.unique())

        #     d = data['Role']
        #     get_role_data = list(d.unique())
        #     role = []
        #     for i in data['Role']:
        #         role.append(i)
        
        #     dashboard2 = dict(Counter(role))
    
        #     keys = list(dashboard2.keys())
        #     values = list(dashboard2.values())
            

        #     specialty_chart = []
        #     for i in data['Sub-Specialty']:
        #         specialty_chart.append(i)
            
        #     dashboard3 = dict(Counter(specialty_chart))

        #     keys1 = list(dashboard3.keys())
        #     values1 = list(dashboard3.values())


        #     site = []
        #     for i in data['Location']:
        #         site.append(i)
            
        #     dashboard6 = dict(Counter(site))

        #     keys2 = list(dashboard6.keys())
        #     values2 = list(dashboard6.values())

        #     if is_admin:
        #         return JsonResponse({'keys': keys, 'values': values, 'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2})
        #     return render(request, 'home/sample.html', {'keys': keys, 'values': values, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty, "get_location":get_location})
        # except:
        #     pass
        
        
        
    
  
    if request.method == 'GET':
        
        
        if not request.user.is_superuser:
            obj = Graphs.objects.filter(user=request.user)
        elif request.method == "GET" and request.user.is_superuser and request.GET.get('user_id'):
            obj = Graphs.objects.filter(user=int(request.GET.get('user_id')))
        else:
            obj = Graphs.objects.filter(user=int(4565465465456))
           
            # if request.GET.get('id') and request.GET.get('is_admin'):
            #     print("AJAX BRO")
            #     obj = Graphs.objects.filter(user=request.GET.get('id'))
            # else:
            #     print("YEAH ELSE ")
            #     obj = Graphs.objects.filter(user=request.GET.get('id'))

        
        if obj.exists():
            obj = obj.last()

        
            file_path = obj.upload.path
            data = read_data(file_path)

            context_di = {}
            staff = {}
            for i in data['Staff']:
                # print(i, "ii")
                context_di[i] =  data[data['Staff'] == i]
                # print(context_di[i],"context_di[i]")
                # print(context_di[i]['Role'], "context_di[i]['Role']")
                # print(Counter(context_di[i]['Role']), "context_di[i]['Role']")
                staff[i] = dict(Counter(context_di[i]['Role']))
            get_roles = data['Role']
            get_roles_data = list(get_roles.unique())
            get_starr = list(staff.values())
            # for h in get_roles_data:
            #     if h not in get_starr:
            #         get_starr[h] = 0
                    
            # print(get_starr, "get_starrget_starr")
            # print(get_roles_data, "get_starr")
            a = data['Staff']
            get_staff = list(a.unique())

            e = data['PGY']
            get_pgy = list(e.unique())

            b = data['Sub-Specialty']
            get_sub_specialty = list(b.unique())

            c = data['Location']
            get_location = list(c.unique())

            d = data['Role']
            get_role_data = list(d.unique())
            df1 = pd.read_excel(file_path, sheet_name='Calculations', header=1, parse_dates=True)
            df = df1.sort_values('Total')
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
            # print(datem,"datemdatem")
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
        
            dashboard23 = dict(Counter(coded_case))
            
            
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
                    'Secondary Assist': secondary_assist[i]
                    })

            datasets = [
                {
                "label": 'Primary Surgeon',
                "backgroundColor": "#398AB9",
                "data": []
                },
                {
                "label": 'First Assist',
                "backgroundColor": "#D8D2CB",
                "data": []
                },
                {
                "label": 'Secondary Assist',
                "backgroundColor": "#1A374D",
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


            keys1 = list(dashboard3.keys())
            values1 = list(dashboard3.values())
            
            site = []
            for i in data['Location']:
                site.append(i)
            
            dashboard16 = dict(Counter(site))
            dashboard6 = (dict(sorted(dashboard16.items(), key=lambda x:x[1],)))
            keys2 = list(dashboard6.keys())
            values2 = list(dashboard6.values())

            context_dict = {}
            roles = {}
            for i in data['Date'].dt.year:
                context_dict[i] =  data[data['Date'].dt.year == i]
                roles[i] = dict(Counter(context_dict[i]['Role']))
            
            # print(roles, "roles")
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

            context = { 'keys':keys , 'values':values,'keys1': keys1, 'values1': values1 , 'keys2': keys2, 'values2': values2, 'final_data': final_final_data, 'labels': labels, 'dashboard23':dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month,"final_data_list":datasets,"names":names, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty, "get_location":get_location,
            "users":User.objects.all().exclude(is_superuser=True),"get_pgy":get_pgy}
            return render(request, 'home/sample.html', context)
        else:
            return render(request, 'home/sample.html',{'users':User.objects.all().exclude(is_superuser=True)})
        
    if request.method == 'POST' :
        # print(request.GET.get('user_id'),"bbb")
        if not request.FILES.get('document') and not request.user.is_superuser:
            obj = Graphs.objects.filter(user=request.user)
            if obj.exists():
                obj = obj.last()
            
                upload_file = obj.upload.path
        elif not request.FILES.get('document') and request.user.is_superuser:
            obj = Graphs.objects.filter(user=request.GET.get('user_id'))
            if obj.exists():
                obj = obj.last()
            
                upload_file = obj.upload.path
                
            
        else:
            upload_file = request.FILES['document']

        # print(upload_file)        
        df1 = pd.read_excel(upload_file, sheet_name='Calculations', header=1, parse_dates=True)
        df = df1.sort_values('Total')
        # file_extension = os.path.splitext(upload_file)[1]

        # valid_extensions = [ ".csv", ".CSV", ".xlsx", ".XLSX", ".xls", ".XLS"]

        # if not file_extension.lower() in valid_extensions:
        #     msg = "Invalid file, select a valid CSV file"
        #     messages.error(request, msg)
        #     return render(request,'home/sample.html')

        #read the file and convert to data frame.
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

        e = data['PGY']
        get_pgy = list(e.unique())

        b = data['Sub-Specialty']
        get_sub_specialty = list(b.unique())

        c = data['Location']
        get_location = list(c.unique())

        d = data['Role']
        get_role_data = list(d.unique())
        get_s =  [int(i) for i in data['PGY']]
        print(get_s, "data['PGY']")
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
            print(get_data_specialty, "get_data_specialty")
            get_g_specialty = data[data["Sub-Specialty"].isin(get_data_specialty)]
            print(get_g_specialty,"get_g")
        if request.POST.getlist("PGY"):
            get_data_p = request.POST.getlist("PGY")
            get_data_pgy = [i.replace(".0", "") for i in get_data_p]
            print(get_data_pgy, "get_data_pgy")
            for i in range(0, len(get_data_pgy)):
                get_data_pgy[i] = int(get_data_pgy[i])
            get_g_pgy = data[data["PGY"].isin(get_data_pgy)]
            print(get_g_pgy, "1st check get_g_pgy")
        
        if set(['Role','Sub-Specialty', 'Location','Date']).issubset(data.columns):
    
            save_obj = Graphs(user=request.user, upload=upload_file)
            save_obj.save()
            if not request.POST.getlist("Staff"):
                names = list(df.Name)
                print(names, "names")
            else:
                print("else part")
                names = get_data_staff
                print(names, "namesss")

            primary_surgeon = list(df['Primary Surgeon']) 
            first_assist = list(df['First Assist'])
            secondary_assist = list(df['Secondary Assist'])

            user_data = []

            for i in range(len(names)):
                user_data.append({
                    'Name': names[i],
                    'Primary Surgeon': primary_surgeon[i], 
                    'First Assist': first_assist[i], 
                    'Secondary Assist': secondary_assist[i]
                    })

            datasets = [
                {
                "label": 'Primary Surgeon',
                "backgroundColor": "#398AB9",
                "data": []
                },
                {
                "label": 'First Assist',
                "backgroundColor": "#D8D2CB",
                "data": []
                },
                {
                "label": 'Secondary Assist',
                "backgroundColor": "#1A374D",
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
            specialty_chart = []
            site =[]
            if request.POST.getlist("PGY"):
                print("yes true")
                print(get_g_pgy,"get_g_pgyget_g_pgy")
                for i in get_g_pgy['Role']:
                    role.append(i)
                
                dashboard1 = dict(Counter(role))
                keys = list(dashboard1.keys())
                values = list(dashboard1.values())
                print(role, "rolerolerole")

                for i in get_g_pgy['Sub-Specialty']:
                    specialty_chart.append(i)
                
                dashboard13 = dict(Counter(specialty_chart))
                dashboard3 = (dict(sorted(dashboard13.items(), key=lambda x:x[1], )))
                keys1 = list(dashboard3.keys())
                values1 = list(dashboard3.values())

                for i in get_g_pgy['Location']:
                    site.append(i)
                
                dashboard16 = dict(Counter(site))
                dashboard6 = (dict(sorted(dashboard16.items(), key=lambda x:x[1],)))


                keys2 = list(dashboard6.keys())
                values2 = list(dashboard6.values())

                context_dict = {}
                roles = {}
                for i in get_g_pgy['Date'].dt.year:
                    context_dict[i] =  get_g_pgy[get_g_pgy['Date'].dt.year == i]
                    roles[i] = dict(Counter(context_dict[i]['Role']))
                print(roles, "roles_get_role")
                labels = []
                role_keys = []
                raw_data = []
                for role in roles:
                    labels.append(role)
                    role_key = list(roles[role].keys())
                    role_keys.append(role_key)
                    raw_data.append(roles[role])
                print(role_keys, "role_keys")
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

                coded_case = []
                for i in get_g_pgy['Coded Case']:
                    coded_case.append(i)
            
                dashboard23 = dict(Counter(coded_case))

                total_cases = len(get_g_pgy)
                current_year = date.today().year
                get_date = get_g_pgy[get_g_pgy['Date'].dt.year == current_year] 

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
                this_year_month = get_g_pgy[get_g_pgy['Date'].dt.to_period('M') == last_months]
                get_g = this_year_month['Role'] == 'Primary Surgeon'
                count_of_last_month = 0
                for i in get_g:
                    if i == True:
                        count_of_last_month+=1
                    else:
                        pass


                today = date.today()
                datem = today.strftime("%Y-%m")
                print(datem,"datemdatem")
                this_year_this_month = get_g_pgy[get_g_pgy['Date'].dt.to_period('M') == datem]
                get_role = this_year_this_month['Role'] == 'Primary Surgeon'
                count_of_this_month = 0
                for i in get_role:
                    if i == True:
                        count_of_this_month+=1
                    else:
                        pass

                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":names, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty,"get_pgy":get_pgy, "get_location":get_location, "dashboard23":dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
                return render(request, 'home/sample.html', context)

            if request.POST.getlist("Role"):
                print("if")
                for i in get_g_role['Role']:
                    role.append(i)
                
                dashboard1 = dict(Counter(role))
                keys = list(dashboard1.keys())
                values = list(dashboard1.values())

                for i in get_g_role['Sub-Specialty']:
                    specialty_chart.append(i)
                
                dashboard13 = dict(Counter(specialty_chart))
                dashboard3 = (dict(sorted(dashboard13.items(), key=lambda x:x[1], )))
                keys1 = list(dashboard3.keys())
                values1 = list(dashboard3.values())

                for i in get_g_role['Location']:
                    site.append(i)
                
                dashboard16 = dict(Counter(site))
                dashboard6 = (dict(sorted(dashboard16.items(), key=lambda x:x[1],)))


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
                        "borderColor": color_line_chart(key),
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
                print(datem,"datemdatem")
                this_year_this_month = get_g_role[get_g_role['Date'].dt.to_period('M') == datem]
                get_role = this_year_this_month['Role'] == 'Primary Surgeon'
                count_of_this_month = 0
                for i in get_role:
                    if i == True:
                        count_of_this_month+=1
                    else:
                        pass

                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":names, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty,"get_pgy":get_pgy, "get_location":get_location, "dashboard23":dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
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
                        "borderColor": color_line_chart(key),
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
                print(datem,"datemdatem")
                this_year_this_month = get_g_specialty[get_g_specialty['Date'].dt.to_period('M') == datem]
                get_role = this_year_this_month['Role'] == 'Primary Surgeon'
                count_of_this_month = 0
                for i in get_role:
                    if i == True:
                        count_of_this_month+=1
                    else:
                        pass


                dashboard23 = dict(Counter(coded_case))
                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":names, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty,"get_pgy":get_pgy, "get_location":get_location, "dashboard23":dashboard23,"total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
                return render(request, 'home/sample.html', context)
                

                
            else:
                for i in data['Sub-Specialty']:
                    specialty_chart.append(i)
                
                dashboard3 = dict(Counter(specialty_chart))
                

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
                        "borderColor": color_line_chart(key),
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
                print(datem,"datemdatem")
                this_year_this_month = get_g_location[get_g_location['Date'].dt.to_period('M') == datem]
                get_role = this_year_this_month['Role'] == 'Primary Surgeon'
                count_of_this_month = 0
                for i in get_role:
                    if i == True:
                        count_of_this_month+=1
                    else:
                        pass
                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":names, "get_staff":get_staff,"get_pgy":get_pgy, "get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty, "get_location":get_location, "dashboard23":dashboard23,"total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
                return render(request, 'home/sample.html', context)
                
            else:
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
                    "borderColor":color_line_chart(key),
                    "backgroundColor": color_line_chart(key),
                    })
          
            final_final_data = {
                "datasets": final_data,
                "labels": labels,
            }



            
            
            context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":names, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty,"get_pgy":get_pgy,  "get_location":get_location, "dashboard23":dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
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

    
    
   
   
