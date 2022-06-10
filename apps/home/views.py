# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from calendar import month
from typing import Counter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

import pandas as pd


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def generate_bar_chart(request):
    
    pandas_data_frame = pd.read_excel('Ortho.xlsx', sheet_name='RAW', header=2, )
    data = pd.DataFrame(pandas_data_frame)

    role = []
    for i in data['Role']:
        role.append(i)
  
    dashboard2 = dict(Counter(role))
    # print(dashboard2)
    keys = list(dashboard2.keys())
    values = list(dashboard2.values())
    
    specialty_chart = []
    for i in data['Sub-Specialty']:
        specialty_chart.append(i)
    
    dashboard3 = dict(Counter(specialty_chart))
    print(dashboard3)

    keys3 = list(dashboard3.keys())
    values3 = list(dashboard3.values())

    _year = []
    for i in data['Date'].dt.year:

        _year.append(i)
    
    dashboard4 = dict(Counter(_year))
    # print(dashboard4)

    _month = []
    for i in data['Date'].dt.month:
            
            _month.append(i)
    dashboard5 = dict(Counter(_month))
    print(dashboard5)


    



    
 
    context = {'keys': keys, 'values': values, 'keys3': keys3, 'values3': values3,  }
    
    
    return render(request, 'home/sample.html', context)
    # data_frame_json = json.loads(pandas_data_frame.to_json())
    # json_data = json.dumps(data_frame_json)
    # print(json_data)
    # role = []
    # for i in range(len(data_frame_json)):
    #     role.append(['Role', data_frame_json[i]['Role']])
    # print(role)
 
    # for i in data_frame_json:
    #     role.append(i['Role'])
    # print(role)
    # role_count = []
    # for i in role:
    #     role_count.append(role.count(i))
    # print(role_count)
    # plt.bar(role, role_count)
    # plt.show()
    # return HttpResponseRedirect(reverse('home:index'))

    # data = pd.read_excel('Ortho.xlsx', sheet_name='RAW', header=2, index_col=0)
    # df = pd.DataFrame(data)
    # data = plt.bar(df['Role'],height=df['Staff'])
    # for i in data:


  


    # print(df)
    # plt.bar(df.index,df['Role'],align='edge', width=-0.4)
  
    # plt.show()
    # return HttpResponse("Hello, world. You're at the home index.")
    




# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))
