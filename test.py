role = {
        2021: {'Secondary Assist': 6, 'First Assist': 2}, 
        2022: {'Primary Surgeon': 2},
        2023: {'Secondary Assist': 2, 'Primary Surgeon': 1}
        }
    
_data = []
year = []
roles_keys = []
for r in role:
    year.append(r)
    roles_keys.append(list(role[r].keys()))
    data = {
        'Secondary Assist': role[r].get('Secondary Assist', 0),
        'First Assist': role[r].get('First Assist', 0),
        'Primary Surgeon': role[r].get('Primary Surgeon', 0)
    }
    
    _data.append(data)
print(year)
print(_data)
print(roles_keys)   


