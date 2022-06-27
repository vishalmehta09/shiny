data  = [{'name': 'Jamal Al-Asiri', 'Primary Surgeon': 3, 'First Assist': 2, 'Secondary Assist': 8}, {'name': 'Krishan Rajaratnam', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 0}, {'name': 'Herman Johal', 'Primary Surgeon': 1, 'First Assist': 6, 'Secondary Assist': 10}, {'name': 'Bill Ristevski', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}, {'name': 'Dale Williams', 'Primary Surgeon': 0, 'First Assist': 0, 'Secondary Assist': 1}, {'name': 'Daniel Tushinski', 'Primary Surgeon': 3, 'First Assist': 14, 'Secondary Assist': 36}, {'name': 'Kajeandra Ravichandran', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 2}, {'name': 'Mitchell Winemaker', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 4}, {'name': 'Kamal Bali', 'Primary Surgeon': 14, 'First Assist': 29, 'Secondary Assist': 13}, {'name': 'Thomas Wood', 'Primary Surgeon': 7, 'First Assist': 5, 'Secondary Assist': 18}, {'name': 'Paul Missiuna', 'Primary Surgeon': 4, 'First Assist': 6, 'Secondary Assist': 0}, {'name': 'Darren de SA', 'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 1}, {'name': 'Olufemi Ayeni', 'Primary Surgeon': 0, 'First Assist': 1, 'Secondary Assist': 2}, {'name': 'Jeffrey Hartman', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, {'name': 'Giuseppe Valente', 'Primary Surgeon': 11, 'First Assist': 3, 'Secondary Assist': 3}, {'name': 'Jimmy Yan', 'Primary Surgeon': 2, 'First Assist': 7, 'Secondary Assist': 0}, {'name': 'Vickas Khanna', 'Primary Surgeon': 5, 'First Assist': 3, 'Secondary Assist': 11}, {'name': 'Anthony Adili', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 28}, {'name': 'Victoria Avram', 'Primary Surgeon': 1, 'First Assist': 3, 'Secondary Assist': 0}, {'name': 'Scott Evans', 'Primary Surgeon': 3, 'First Assist': 0, 'Secondary Assist': 0}, {'name': 'Matthew Denkers', 'Primary Surgeon': 0, 'First Assist': 3, 'Secondary Assist': 2}]


#shorting data by Primary Surgeon
data1 = data.sort(key=lambda x: x['Primary Surgeon'], reverse=True)

# shorting data by First Assist
data2 = data1.sort(key=lambda x: x['First Assist'], reverse=True)
print(data2)


