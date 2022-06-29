

from tkinter import E
from traceback import print_tb
from unittest import result
from urllib.parse import uses_params
from django.contrib.auth.models import User
from apps.authentication.models import *
from typing import Counter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from .models import Graphs
import pandas as pd
import random
from django.contrib import messages
from datetime import date
from datetime import timedelta
from django.contrib.auth.hashers import make_password


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
        institute = Institution.objects.all()
        supervisor = Supervisor.objects.all()
        print(institute, "institute")
        if not request.user.is_superuser:
            obj = Graphs.objects.filter(user=request.user)
        elif request.method == "GET" and request.user.is_superuser and request.GET.get('user_id'):
            obj = Graphs.objects.filter(user=int(request.GET.get('user_id')))
        else:
            obj = Graphs.objects.filter(user=int(4565465465456))

        
        if obj.exists():
            obj = obj.last()

            institute = Institution.objects.all()
            supervisor = Supervisor.objects.all()
            file_path = obj.upload.path
            data = read_data(file_path)

            context_di = {}
            staff = {}
            
            for i in data['Staff']:
                context_di[i] =  data[data['Staff'] == i]


                staff[i] = dict(Counter(context_di[i]['Role']))
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
            # print(only_final_data)

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
            print(roles, "rolesss")
        
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

            context = { 'keys':keys , 'values':values,'keys1': keys1, 'values1': values1 , 'keys2': keys2, 'values2': values2, 'final_data': final_final_data, 'labels': labels, 'dashboard23':dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month,"final_data_list":datasets,"names":name_set, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty, "get_location":get_location,
            "users":NewUser.objects.all().exclude(is_superuser=True),"get_pgy":get_pgy, "institute":institute, "supervisor":supervisor}
            return render(request, 'home/sample.html', context)
        else:
            return render(request, 'home/sample.html',{'users':NewUser.objects.all().exclude(is_superuser=True),"institute":institute, "supervisor":supervisor})
        
    if request.method == 'POST' :
        institute = Institution.objects.all()
        supervisor = Supervisor.objects.all()
        print(institute, "institute")
        # print(request.GET.get('user_id'),"bbb")
        if not request.FILES.get('document') and not request.user.is_superuser:
            obj = Graphs.objects.filter(user=request.user)
            if obj.exists():
                obj = obj.last()

                upload_file = obj.upload.path

        elif not request.FILES.get('document') and request.POST.get("username") and not request.POST.get("email"):

            username=request.POST.get("username")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            user = NewUser.objects.create(username=username)
            if password == confirm_password:
                user.password=make_password(password)
                user.is_supervisor=True
                user.save()
                supervisor = Supervisor.objects.create(username=username)
                messages.success(request, "Supervisor created successfully")
                return redirect("/")
            else:
                messages.error(request, "Password doesn't matched")
                return redirect("/")
        
        elif not request.FILES.get('document') and request.POST.get("institute") and not request.POST.get("email"):

            institute=request.POST.get("institute")
            user = Institution.objects.create(institute=institute)
            messages.success(request, "Institute created successfully")
            return redirect("/")

        elif not request.FILES.get('document') and request.POST.get("email"):
            print("true case")
            print(request.POST.values,"valuess")
            email=request.POST.get("email")
            username=request.POST.get("username")
            first_name=request.POST.get("first_name")
            last_name=request.POST.get("last_name")
            institute=request.POST.get("institute")
            supervisor=request.POST.get("supervisor")
            password=request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            try:
                obj_institute = Institution.objects.get(institute=institute)
            except:
                messages.error(request, "Institute doesn't exists")
                return redirect('/')
            try:
                obj_supervisor = Supervisor.objects.get(username=supervisor)
            except:
                messages.error(request, "Supervisor doesn't exists")
                return redirect('/')
            if NewUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('/')
            else:
                username=username
            if NewUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                email=email
            users = NewUser.objects.create(email=email,username=username,first_name=first_name,last_name=last_name,institute=obj_institute,supervisor=obj_supervisor)
            if password == confirm_password:
                users.password=make_password(password)
                users.is_active=True
                users.save()
                messages.success(request, "User created successfully")
                return redirect("/")
            else:
                messages.error(request, "Password doesn't matched")
                return redirect("/")
            
        elif not request.FILES.get('document') and request.user.is_superuser:
            obj = Graphs.objects.filter(user=request.GET.get('user_id'))
            if obj.exists():
                obj = obj.last()
                upload_file = obj.upload.path
        else:
            upload_file = request.FILES['document']

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
        # print(get_s, "data['PGY']")
        if request.POST.getlist("Staff"):
            get_data_staff = request.POST.getlist("Staff")
            get_g_staff = data[data["Staff"].isin(get_data_staff)]
            print(get_g_staff, "get_g_staff")
        if request.POST.getlist("Role"):
            get_data_role = request.POST.getlist("Role")
            get_g_role = data[data["Role"].isin(get_data_role)]
        if request.POST.getlist("Location") :
            get_data_location = request.POST.getlist("Location")
            get_g_location = data[data["Location"].isin(get_data_location)]
        if request.POST.getlist("Sub-Specialty"):
            get_data_specialty = request.POST.getlist("Sub-Specialty")
            # print(get_data_specialty, "get_data_specialty")
            get_g_specialty = data[data["Sub-Specialty"].isin(get_data_specialty)]
            # print(get_g_specialty,"get_g")
        if request.POST.getlist("PGY"):
            get_data_p = request.POST.getlist("PGY")
            get_data_pgy = [i.replace(".0", "") for i in get_data_p]
            # print(get_data_pgy, "get_data_pgy")
            for i in range(0, len(get_data_pgy)):
                get_data_pgy[i] = int(get_data_pgy[i])
            get_g_pgy = data[data["PGY"].isin(get_data_pgy)]
            # print(get_g_pgy, "1st check get_g_pgy")

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
      
            else:
                names = get_data_staff
          
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
                # print(d)
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

            if request.POST.getlist("Staff"):
                context_dib = {}

                staffs = {}

                for i in get_g_staff['Staff']:
                    context_dib[i] =  get_g_staff[get_g_staff['Staff'] == i]
                    staffs[i] = dict(Counter(context_dib[i]['Role']))

                print(get_g_staff['Staff'], "staffs")
                name_set = []
                for i in range(len(staffs)):
                    name_set.append(list(staffs.keys())[i])

                only_final_data = []

                for d in staffs:
                    final_data = {
                        "name": d,
                        "Primary Surgeon": staffs[d].get('Primary Surgeon', 0),
                        "First Assist": staffs[d].get('First Assist', 0),
                        "Secondary Assist": staffs[d].get('Secondary Assist', 0),
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
                    # print(d)
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
                role=[]
                for i in get_g_staff['Role']:
                    role.append(i)
                
                dashboard1 = dict(Counter(role))
                keys = list(dashboard1.keys())
                values = list(dashboard1.values())
                # print(role, "rolerolerole")
                specialty_chart =[]
                for i in get_g_staff['Sub-Specialty']:
                    specialty_chart.append(i)
                
                dashboard13 = dict(Counter(specialty_chart))
                dashboard3 = (dict(sorted(dashboard13.items(), key=lambda x:x[1], )))
                keys1 = list(dashboard3.keys())
                values1 = list(dashboard3.values())
                site =[]
                for i in get_g_staff['Location']:
                    site.append(i)
                
                dashboard16 = dict(Counter(site))
                dashboard6 = (dict(sorted(dashboard16.items(), key=lambda x:x[1],)))


                keys2 = list(dashboard6.keys())
                values2 = list(dashboard6.values())

                context_dict = {}
                roles = {}
                for i in get_g_staff['Date'].dt.year:
                    context_dict[i] =  get_g_staff[get_g_staff['Date'].dt.year == i]
                    roles[i] = dict(Counter(context_dict[i]['Role']))
                # print(roles, "roles_get_role")
                labels = []
                role_keys = []
                raw_data = []
                for role in roles:
                    labels.append(role)
                    role_key = list(roles[role].keys())
                    role_keys.append(role_key)
                    raw_data.append(roles[role])
                # print(role_keys, "role_keys")
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
                for i in get_g_staff['Coded Case']:
                    coded_case.append(i)
            
                dashboard23 = dict(Counter(coded_case))

                total_cases = len(get_g_staff)
                current_year = date.today().year
                get_date = get_g_staff[get_g_staff['Date'].dt.year == current_year] 

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
                this_year_month = get_g_staff[get_g_staff['Date'].dt.to_period('M') == last_months]
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
                this_year_this_month = get_g_staff[get_g_staff['Date'].dt.to_period('M') == datem]
                get_role = this_year_this_month['Role'] == 'Primary Surgeon'
                count_of_this_month = 0
                for i in get_role:
                    if i == True:
                        count_of_this_month+=1
                    else:
                        pass

                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":name_set, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty,"get_pgy":get_pgy, "get_location":get_location, "dashboard23":dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
                return render(request, 'home/sample.html', context)

            role = []
            specialty_chart = []
            site =[]
            if request.POST.getlist("PGY"):
                # print("yes true")
                # print(get_g_pgy,"get_g_pgyget_g_pgy")
                for i in get_g_pgy['Role']:
                    role.append(i)
                
                dashboard1 = dict(Counter(role))
                keys = list(dashboard1.keys())
                values = list(dashboard1.values())
                # print(role, "rolerolerole")

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
                # print(roles, "roles_get_role")
                labels = []
                role_keys = []
                raw_data = []
                for role in roles:
                    labels.append(role)
                    role_key = list(roles[role].keys())
                    role_keys.append(role_key)
                    raw_data.append(roles[role])
                # print(role_keys, "role_keys")
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
                # print(datem,"datemdatem")
                this_year_this_month = get_g_pgy[get_g_pgy['Date'].dt.to_period('M') == datem]
                get_role = this_year_this_month['Role'] == 'Primary Surgeon'
                count_of_this_month = 0
                for i in get_role:
                    if i == True:
                        count_of_this_month+=1
                    else:
                        pass
                context_dib = {}

                staffs = {}

                for i in get_g_pgy['Staff']:
                    context_dib[i] =  get_g_pgy[get_g_pgy['Staff'] == i]
                    staffs[i] = dict(Counter(context_dib[i]['Role']))

                print(get_g_pgy['Staff'], "staffs")
                name_set = []
                for i in range(len(staffs)):
                    name_set.append(list(staffs.keys())[i])
                print(name_set,"name_set")
                only_final_data = []

                for d in staffs:
                    final_data = {
                        "name": d,
                        "Primary Surgeon": staffs[d].get('Primary Surgeon', 0),
                        "First Assist": staffs[d].get('First Assist', 0),
                        "Secondary Assist": staffs[d].get('Secondary Assist', 0),
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
                    # print(d)
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

                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":name_set, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty,"get_pgy":get_pgy, "get_location":get_location, "dashboard23":dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
                return render(request, 'home/sample.html', context)
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

                context_dib = {}

                staffs = {}

                for i in get_g_role['Staff']:
                    context_dib[i] =  get_g_role[get_g_role['Staff'] == i]
                    staffs[i] = dict(Counter(context_dib[i]['Role']))

                print(get_g_role['Staff'], "staffs")
                name_set = []
                for i in range(len(staffs)):
                    name_set.append(list(staffs.keys())[i])

                only_final_data = []

                for d in staffs:
                    final_data = {
                        "name": d,
                        "Primary Surgeon": staffs[d].get('Primary Surgeon', 0),
                        "First Assist": staffs[d].get('First Assist', 0),
                        "Secondary Assist": staffs[d].get('Secondary Assist', 0),
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
                    # print(d)
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

                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets,"names":name_set, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty,"get_pgy":get_pgy, "get_location":get_location, "dashboard23":dashboard23, "total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
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
                role=[]
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
                
                context_dib = {}

                staffs = {}

                for i in get_g_specialty['Staff']:
                    context_dib[i] =  get_g_specialty[get_g_specialty['Staff'] == i]
                    staffs[i] = dict(Counter(context_dib[i]['Role']))

                # print(get_g_specialty['Staff'], "staffs")
                name_set = []
                for i in range(len(staffs)):
                    name_set.append(list(staffs.keys())[i])

                only_final_data = []

                for d in staffs:
                    final_data = {
                        "name": d,
                        "Primary Surgeon": staffs[d].get('Primary Surgeon', 0),
                        "First Assist": staffs[d].get('First Assist', 0),
                        "Secondary Assist": staffs[d].get('Secondary Assist', 0),
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
                    # print(d)
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


                dashboard23 = dict(Counter(coded_case))
                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty,"get_pgy":get_pgy, "get_location":get_location, "dashboard23":dashboard23,"total_cases":total_cases, "names":name_set,"count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
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

                context_dib = {}

                staffs = {}

                for i in get_g_location['Staff']:
                    context_dib[i] =  get_g_location[get_g_location['Staff'] == i]
                    staffs[i] = dict(Counter(context_dib[i]['Role']))

                print(get_g_location['Staff'], "staffs")
                name_set = []
                for i in range(len(staffs)):
                    name_set.append(list(staffs.keys())[i])

                only_final_data = []

                for d in staffs:
                    final_data = {
                        "name": d,
                        "Primary Surgeon": staffs[d].get('Primary Surgeon', 0),
                        "First Assist": staffs[d].get('First Assist', 0),
                        "Secondary Assist": staffs[d].get('Secondary Assist', 0),
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
                    # print(d)
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
                context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets, "get_staff":get_staff,"get_pgy":get_pgy, "get_role_data":get_role_data, "names":name_set,"get_sub_specialty":get_sub_specialty, "get_location":get_location, "dashboard23":dashboard23,"total_cases":total_cases, "count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month}
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
            
            context = {"keys":keys,"values":values,'keys1': keys1, 'values1': values1, 'keys2': keys2, 'values2': values2 , 'final_data': final_final_data, 'labels': labels,"final_data_list":datasets, "get_staff":get_staff,"get_role_data":get_role_data, "get_sub_specialty":get_sub_specialty,"get_pgy":get_pgy,  "get_location":get_location, "dashboard23":dashboard23, "total_cases":total_cases, "names":name_set,"count_of_current_year":count_of_current_year, "count_of_current":count_of_current,"count_of_last_month":count_of_last_month, 'count_of_this_month':count_of_this_month,'institute':institute, 'supervisor':supervisor}
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

    
def change_password(request): 
    if request.method == "POST": 
        current_user = request.user.username
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        user = NewUser.objects.get(username= current_user)
        if user:
            if password == confirm_password:
                user.password = make_password(password)
                user.save()
                messages.success(request, "successfully saved")
                return redirect('change_password')
            else:
                messages.error(request, "password and confirm password not matched")
                return redirect('change_password')

        else:
            messages.error(request, "Invalid user")
            return redirect('change_password')
    else:
        return render(request, 'home/change_password.html')
   
   