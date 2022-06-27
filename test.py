data  = [{'name': 'Jamal Al-Asiri', 'Primary Surgeon': 3, 'First Assist': 2, 'Secondary Assist': 8},
 {'name': 'Krishan Rajaratnam', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 0}, 
 {'name': 'Herman Johal', 'Primary Surgeon': 1, 'First Assist': 6, 'Secondary Assist': 10},
  {'name': 'Bill Ristevski', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}, {'name': 'Dale Williams', 'Primary Surgeon': 0, 'First Assist': 0, 'Secondary Assist': 1}, {'name': 'Daniel Tushinski', 'Primary Surgeon': 3, 'First Assist': 14, 'Secondary Assist': 36}, {'name': 'Kajeandra Ravichandran', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 2}, {'name': 'Mitchell Winemaker', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 4}, {'name': 'Kamal Bali', 'Primary Surgeon': 14, 'First Assist': 29, 'Secondary Assist': 13}, {'name': 'Thomas Wood', 'Primary Surgeon': 7, 'First Assist': 5, 'Secondary Assist': 18}, {'name': 'Paul Missiuna', 'Primary Surgeon': 4, 'First Assist': 6, 'Secondary Assist': 0}, {'name': 'Darren de SA', 'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 1}, {'name': 'Olufemi Ayeni', 'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 2}, {'name': 'Jeffrey Hartman', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, {'name': 'Giuseppe Valente', 'Primary Surgeon': 11, 'First Assist': 3, 'Secondary Assist': 3}, {'name': 'Jimmy Yan', 'Primary Surgeon': 2, 'First Assist': 7, 'Secondary Assist': 0}, {'name': 'Vickas Khanna', 'Primary Surgeon': 5, 'First Assist': 3, 'Secondary Assist': 11}, {'name': 'Anthony Adili', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 28}, {'name': 'Victoria Avram', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, {'name': 'Scott Evans', 'Primary Surgeon': 3, 'First Assist': 0, 'Secondary Assist': 0}, {'name': 'Matthew Denkers', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}]
# data = {'Jamal Al-Asiri': {'Secondary Assist': 8, 'First Assist': 2, 'Primary Surgeon': 3}, 'Krishan Rajaratnam': {'First Assist': 3}, 'Herman Johal': {'Secondary Assist': 10, 'First Assist': 6, 'Primary Surgeon': 1}, 'Bill Ristevski': {'Secondary Assist': 2, 'First Assist': 3}, 'Dale Williams': {'Secondary Assist': 1}, 'Daniel Tushinski': {'Secondary Assist': 36, 'First Assist': 14, 'Primary Surgeon': 3}, 'Kajeandra Ravichandran': {'First Assist': 3, 'Secondary Assist': 2, 'Primary Surgeon': 1}, 'Mitchell Winemaker': {'Secondary Assist': 4, 'First Assist': 3, 'Primary Surgeon': 1}, 'Kamal Bali': {'Secondary Assist': 13, 'First Assist': 29, 'Primary Surgeon': 14}, 'Thomas Wood': {'Secondary Assist': 18, 'Primary Surgeon': 7, 'First Assist': 5}, 'Paul Missiuna': {'First Assist': 6, 'Primary Surgeon': 4}, 'Darren de SA': {'Secondary Assist': 1, 'First Assist': 1}, 'Olufemi Ayeni': {'Secondary Assist': 2, 'First Assist': 1}, 'Jeffrey Hartman': {'First Assist': 3, 'Primary Surgeon': 1}, 'Giuseppe Valente': {'Secondary Assist': 3, 'First Assist': 3, 'Primary Surgeon': 11}, 'Jimmy Yan': {'First Assist': 7, 'Primary Surgeon': 2}, 'Vickas Khanna': {'Primary Surgeon': 5, 'Secondary Assist': 11, 'First Assist': 3}, 'Anthony Adili': {'Secondary Assist': 28, 'First Assist': 3, 'Primary Surgeon': 1}, 'Victoria Avram': {'First Assist': 3, 'Primary Surgeon': 1}, 'Scott Evans': {'Primary Surgeon': 3}, 'Matthew Denkers': {'First Assist': 3, 'Secondary Assist': 2}}
lists = []

for i in data:
    total = i['Primary Surgeon'] + i['First Assist'] + i['Secondary Assist']
    i['Total'] = total
    lists.append(i)
  
# print(lists)
shorted_data = sorted(lists, key=lambda x: x['Total'], reverse=True)
name_Set = []
for i in shorted_data:
    name_Set.append(i['name'])
print(name_Set)


