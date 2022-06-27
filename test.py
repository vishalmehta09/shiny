data = {'Jamal Al-Asiri': {'Secondary Assist': 8, 'First Assist': 2, 'Primary Surgeon': 3}, 'Krishan Rajaratnam': {'First Assist': 3}, 'Herman Johal': {'Secondary Assist': 10, 'First Assist': 6, 'Primary Surgeon': 1}, 'Bill Ristevski': {'Secondary Assist': 2, 'First Assist': 3}, 'Dale Williams': {'Secondary Assist': 1}, 'Daniel Tushinski': {'Secondary Assist': 36, 'First Assist': 14, 'Primary Surgeon': 3}, 'Kajeandra Ravichandran': {'First Assist': 3, 'Secondary Assist': 2, 'Primary Surgeon': 1}, 'Mitchell Winemaker': {'Secondary Assist': 4, 'First Assist': 3, 'Primary Surgeon': 1}, 'Kamal Bali': {'Secondary Assist': 13, 'First Assist': 29, 'Primary Surgeon': 14}, 'Thomas Wood': {'Secondary Assist': 18, 'Primary Surgeon': 7, 'First Assist': 5}, 'Paul Missiuna': {'First Assist': 6, 'Primary Surgeon': 4}, 'Darren de SA': {'Secondary Assist': 1, 'First Assist': 1}, 'Olufemi Ayeni': {'Secondary Assist': 2, 'First Assist': 1}, 'Jeffrey Hartman': {'First Assist': 3, 'Primary Surgeon': 1}, 'Giuseppe Valente': {'Secondary Assist': 3, 'First Assist': 3, 'Primary Surgeon': 11}, 'Jimmy Yan': {'First Assist': 7, 'Primary Surgeon': 2}, 'Vickas Khanna': {'Primary Surgeon': 5, 'Secondary Assist': 11, 'First Assist': 3}, 'Anthony Adili': {'Secondary Assist': 28, 'First Assist': 3, 'Primary Surgeon': 1}, 'Victoria Avram': {'First Assist': 3, 'Primary Surgeon': 1}, 'Scott Evans': {'Primary Surgeon': 3}, 'Matthew Denkers': {'First Assist': 3, 'Secondary Assist': 2}}

only_final_data = []
for d in data:
    final_data = {
        "name": d,
        
        "Primary Surgeon": data[d].get('Primary Surgeon', 0),
        "First Assist": data[d].get('First Assist', 0),
        "Secondary Assist": data[d].get('Secondary Assist', 0),
 
    }
   
    only_final_data.append(final_data)
print(only_final_data)

# frzi

[{'name': 'Jamal Al-Asiri', 'Primary Surgeon': 3, 'First Assist': 2, 'Secondary Assist': 8}, 
{'name': 'Krishan Rajaratnam', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 0}, 
{'name': 'Herman Johal', 'Primary Surgeon': 1, 'First Assist': 6, 'Secondary Assist': 10}
, {'name': 'Bill Ristevski', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}
, {'name': 'Dale Williams', 'Primary Surgeon': 0, 'First Assist': 0, 'Secondary Assist': 1}, 
{'name': 'Daniel Tushinski', 'Primary Surgeon': 3, 'First Assist': 14, 'Secondary Assist': 36},
 {'name': 'Kajeandra Ravichandran', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 2},
  {'name': 'Mitchell Winemaker', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 4},
   {'name': 'Kamal Bali', 'Primary Surgeon': 14, 'First Assist': 29, 'Secondary Assist': 13},
    {'name': 'Thomas Wood', 'Primary Surgeon': 7, 'First Assist': 5, 'Secondary Assist': 18}, {'name': 'Paul Missiuna', 'Primary Surgeon': 4, 'First Assist': 6, 'Secondary Assist': 0}, {'name': 'Darren de SA', 'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 1}, {'name': 'Olufemi Ayeni', 'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 2}, {'name': 'Jeffrey Hartman', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, {'name': 'Giuseppe Valente', 'Primary Surgeon': 11, 'First Assist': 3, 'Secondary Assist': 3}, {'name': 'Jimmy Yan', 'Primary Surgeon': 2, 'First Assist': 7, 'Secondary Assist': 0}, {'name': 'Vickas Khanna', 'Primary Surgeon': 5, 'First Assist': 3, 'Secondary Assist': 11}, {'name': 'Anthony Adili', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 28}, {'name': 'Victoria Avram', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, {'name': 'Scott Evans', 'Primary Surgeon': 3, 'First Assist': 0, 'Secondary Assist': 0}, {'name': 'Matthew Denkers', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}]


[{'label': 'Primary Surgeon', 'backgroundColor': '#398AB9', 
'data': [3, 0, 1, 0, 0, 3, 1, 1, 14, 7, 4, 0, 0, 1, 11, 2, 5, 1, 1, 3, 0]},
 {'label': 'First Assist', 'backgroundColor': '#D8D2CB', 
 'data': [2, 3, 6, 3, 0, 14, 3, 3, 29, 5, 6, 1, 1, 3, 3, 7, 3, 3, 3, 0, 3]},
  {'label': 'Secondary Assist', 'backgroundColor': '#1A374D', 
  'data': [8, 0, 10, 2, 1, 36, 2, 4, 13, 18, 0, 1, 2, 0, 3, 0, 11, 28, 0, 0, 2]}]



# correct way - 
[{'Name': 'Kamal Bali', 'Primary Surgeon': 14, 'First Assist': 29, 'Secondary Assist': 13}, 
{'Name': 'Daniel Tushinski', 'Primary Surgeon': 3, 'First Assist': 14, 'Secondary Assist': 36},
 {'Name': 'Anthony Adili', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 28},
  {'Name': 'Thomas Wood', 'Primary Surgeon': 7, 'First Assist': 5, 'Secondary Assist': 18},
   {'Name': 'Vickas Khanna', 'Primary Surgeon': 5, 'First Assist': 3, 'Secondary Assist': 11},
    {'Name': 'Giuseppe Valente', 'Primary Surgeon': 11, 'First Assist': 3, 'Secondary Assist': 3}, 
    {'Name': 'Herman Johal', 'Primary Surgeon': 1, 'First Assist': 6, 'Secondary Assist': 10},
     {'Name': 'Jamal Al-Asiri', 'Primary Surgeon': 3, 'First Assist': 2, 'Secondary Assist': 8},
      {'Name': 'Paul Missiuna', 'Primary Surgeon': 4, 'First Assist': 6, 'Secondary Assist': 0}, {'Name': 'Jimmy Yan', 'Primary Surgeon': 2, 'First Assist': 7, 'Secondary Assist': 0}, {'Name': 'Mitchell Winemaker', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 4}, {'Name': 'Kajeandra Ravichandran', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 2}, {'Name': 'Bill Ristevski', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}, {'Name': 'Matthew Denkers', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}, {'Name': 'Jeffrey Hartman', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, {'Name': 'Victoria Avram', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, {'Name': 'Krishan Rajaratnam', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 0}, {'Name': 'Olufemi Ayeni', 'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 2}, {'Name': 'Scott Evans', 'Primary Surgeon': 3, 'First Assist': 0, 'Secondary Assist': 0}, {'Name': 'Darren de SA', 'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 1}, {'Name': 'Dale Williams', 'Primary Surgeon': 0, 'First Assist': 0, 'Secondary Assist': 1}]



  [{'label': 'Primary Surgeon', 'backgroundColor': '#398AB9', 
  'data': [14, 3, 1, 7, 5, 11, 1, 3, 4, 2, 1, 1, 0, 0, 1, 1, 0, 0, 3, 0, 0]},
   {'label': 'First Assist', 'backgroundColor': '#D8D2CB', 
   'data': [29, 14, 3, 5, 3, 3, 6, 2, 6, 7, 3, 3, 3, 3, 3, 3, 3, 1, 0, 1, 0]},
    {'label': 'Secondary Assist', 'backgroundColor': '#1A374D',
     'data': [13, 36, 28, 18, 11, 3, 10, 8, 0, 0, 4, 2, 2, 2, 0, 0, 0, 2, 0, 1, 1]}]