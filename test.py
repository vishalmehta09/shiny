data = {'Daniel Tushinski': {'Primary Surgeon': 3, 'First Assist': 14, 'Secondary Assist': 36}, 'Anthony Adili': {'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 28}, 'Kamal Bali': {'Primary Surgeon': 14, 'First Assist': 29, 'Secondary Assist': 13}, 'Thomas Wood': {'Primary Surgeon': 7, 'First Assist': 5, 'Secondary Assist': 18}, 'Vickas Khanna': {'Primary Surgeon': 5, 'First Assist': 3, 'Secondary Assist': 11}, 'Giuseppe Valente': {'Primary Surgeon': 11, 'First Assist': 3, 'Secondary Assist': 3}, 'Herman Johal': {'Primary Surgeon': 1, 'First Assist': 6, 'Secondary Assist': 10}, 'Jamal Al-Asiri': {'Primary Surgeon': 3, 'First Assist': 2, 'Secondary Assist': 8}, 'Paul Missiuna': {'Primary Surgeon': 4, 'First Assist': 6, 'Secondary Assist': 0}, 'Jimmy Yan': {'Primary Surgeon': 2, 'First Assist': 7, 'Secondary Assist': 0}, 'Bill Ristevski': {'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}, 'Matthew Denkers': {'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}, 'Mitchell Winemaker': {'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 4}, 'Jeffrey Hartman': {'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, 'Victoria Avram': {'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, 'Krishan Rajaratnam': {'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 0}, 'Kajeandra Ravichandran': {'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 2}, 'Olufemi Ayeni': {'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 2}, 'Darren de SA': {'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 1}, 'Scott Evans': {'Primary Surgeon': 3, 'First Assist': 0, 'Secondary Assist': 0}, 'Dale Williams': {'Primary Surgeon': 0, 'First Assist': 0, 'Secondary Assist': 1}}


final_data_list = []
for i in data:
    final_data ={
            "datasets": {
            "label": list(data[i].keys()),
            "data": list(data[i].values())
            }
        }

    final_data_list.append(final_data)
    
print(final_data_list)


